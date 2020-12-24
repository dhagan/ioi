#!/usr/bin/perl

################################################################################
#
#       File Name: emailer.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/2005      M. Smith        Created this file
#       03/29/2007      B. Scarborough  Modified sendMails() to use generic sendMail function
################################################################################

use DBI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";

if(param('submit'))
{
	sendMails();
} elsif ( param('filterTutorial') ) {
	filterTutorial();
} elsif ( param('viewFilterList') ) {
	viewFilterList();
} else {
	createEmail();
}
sub createEmail()
{
	print header();
	background();
	bodyAndLoad();
	tableHead('65%');
	print "
		<tr><td>From</td><td>";
			techDropDown(); 
		print "</td></tr>
		<form name='email' method='post'>
		<input type='hidden' name='verify' value='YES'>
		   <tr><td>Filter Expression</td><td><input type='text' name='filter' size='50'> <a href='emailer.cgi?filterTutorial=yes'>Using filter expressions</a>
		   <input type='button' name='testFilterExpression' onclick='checkFilterUsers()'></td></tr>
		   <tr><td>Subject</td><td><input type='text' name='subject' size='50'></td></tr>
		   <tr><td>Body</td><td><textarea name='body' rows='20' cols='60'></textarea></td></tr>
		   <tr><td colspan='2' align='center'>Available Keywords</td></tr>
		   <tr><td>Firstname</td><td>[FIRSTNAME]</td></tr>
		   <tr><td>Lastname</td><td>[LASTNAME]</td></tr>
		   <tr><td>Company Name</td><td>[COMPANY]</td></tr>
		   <tr><td># of open tickets</td><td>[OPEN_TICKET_COUNT]</td></tr>
		   <tr><td># of closed tickets</td><td>[CLOSED_TICKET_COUNT]</td></tr>
		   <tr><td># of pending tickets</td><td>[PENDING_TICKET_COUNT]</td></tr>
		   <tr><td>Pending ticket subjects</td><td>[PENDING_TICKET_SUBJECTS]</td></tr>
		   <tr><td>Contract Type</td><td>[CONTRACT_TYPE]</td></tr>
		   <tr><td>Contract Expiration Date</td><td>[CONTRACT_EXPIRATION]</td></tr>
		   <tr><td>User Login</td><td>[USER_LOGIN]</td></tr>
		   <tr><td>Password</td><td>[PASSWORD]</td></tr>
		   <tr><td>Company Products</td><td>[COMPANY_PRODUCTS]</td></tr>
		   <tr><td colspan='2'><div align='center'><input type='submit' name='submit' value='Verify Email'></div></td></tr>
		   </table>
		   </form>";
	print end_html();
}


sub sendMails()
{
	print header();
	my %products;
	my $productsNameString;
	my $productWhereString;
	my $pendingTicketSubjects;
	my $dbh = getDBConnection();
	my $i = 0;
	my $subject = param('subject');
	my $body = param('body');
	my $originalBody = $body;
	my $filter = param('filter');
	my $verify = param('verify');
	$filter =~ s/ISEQUALTO/LIKE/g; 
	#my $filterStatement = "SELECT DISTINCT sub_login FROM users JOIN company JOIN contract JOIN product
	#				      WHERE product.prod_comp_link = company.comp_case_num AND users.sub_comp_link = company.comp_case_num AND contract.contract_comp_link = company.comp_case_num and $filter";
	#my $filterExpression = $dbh->prepare($filterStatement);
	#my $count = $filterExpression->execute();
	#print $count . "<p>";
	#print $filter;
	#while ( ($sub_login) = $filterExpression->fetchrow_array()) {
	#	print $sub_login . "<br>";
	#	push @users, $sub_login;
	#}
	my $sth = $dbh->prepare("SELECT DISTINCT sub_name,sub_e_mail,sub_login,sub_password,comp_name,contract_type,contract_date_expired,sub_comp_link FROM users JOIN company JOIN contract JOIN product
				WHERE company.comp_case_num = users.sub_comp_link AND product.prod_comp_link = company.comp_case_num AND company.comp_case_num = contract.contract_comp_link AND sub_access = 'Active'") if (!$filter);
	my $sth = $dbh->prepare("SELECT DISTINCT sub_name,sub_e_mail,sub_login,sub_password,comp_name,contract_type,contract_date_expired,sub_comp_link FROM users JOIN company JOIN contract JOIN product
				WHERE company.comp_case_num = users.sub_comp_link AND product.prod_comp_link = company.comp_case_num AND company.comp_case_num = contract.contract_comp_link AND sub_access = 'Active' and $filter") if ($filter);
	
	$sth->execute();
	while(((my $name,my $email,my $login,my $password, my $company_name, my $contract_type, my $contract_exp_date,my $sub_comp_link) = $sth->fetchrow_array()))
	{
		$productNameString = "";
		my $productStatement = $dbh->prepare("SELECT prod_name,prod_version,prod_case_num FROM product WHERE prod_comp_link = '$sub_comp_link'");
		$productStatement->execute();
		$productWhereString = ();
		while((my $product_name, my $product_version,my $product_link) = $productStatement->fetchrow_array()) {
			$products{$product_name} = $product_version;
			$productNameString .= "$product_name, ";
			if ($productWhereString) {	
				$productWhereString .= "or prob_prod_link = '$product_link' ";
			} else {
				$productWhereString = "and (prob_prod_link = '$product_link' ";
			}
		}
		$productNameString =~ s/, $//g;
		$productWhereString .= ")" if ($productWhereString);
		my $openTickets = $dbh->prepare("SELECT count(case_num) FROM problems WHERE status = 'Open' $productWhereString");
		$openTickets->execute();
		my $openTicketsCount = $openTickets->fetchrow_array();
		my $closedTickets = $dbh->prepare("SELECT count(case_num) FROM problems WHERE status = 'Closed' $productWhereString");
		$closedTickets->execute();
		my $closedTicketCount = $closedTickets->fetchrow_array();
		my $pendingTicketsCount = 0;
		if ( $productWhereString ) {
			my $pendingTickets = $dbh->prepare("SELECT short_desc FROM problems WHERE (status = 'Pending IOI' or status = 'Pending Client') $productWhereString");
			$pendingTickets->execute();
			$pendingTicketSubjects = "";
			while ((my $short_desc) = $pendingTickets->fetchrow_array()) {
				$pendingTicketsCount++;
				$pendingTicketSubjects .= "$pendingTicketsCount) $short_desc\n";
			}
		}
		
		my @firstAndLastName = split(/ /,$name);
		print "---------------------------------------------------------------------------------------------<br>
		Name: $firstAndLastName[0] $firstAndLastName[1]<br>
		Email: $email<br>
		Login: $login<br>
		Password: $password<br>
		Company Name: $company_name<br>
		Contract Type: $contract_type<br>
		Contract Exp Date: $contract_exp_date<br>
		Products: $productNameString<br>
		Open Ticket Count: $openTicketsCount<br>
		Closed Ticket Count: $closedTicketCount<br>
		Pending Ticket Count:$pendingTicketsCount<br>
		Pending Ticket Subjects: $pendingTicketSubjects<br>
		Body: $body<br>
		-----------------------------------------------------------------------------------------------------<br>";
		$i++;
		my @name = split(/ /,$name);
		my $firstname = @name[0];
		my $lastname = @name[1];
		eval
		{
			$body =~ s/\[FIRSTNAME\]/$firstAndLastName[0]/g;
			$body =~ s/\[LASTNAME\]/$firstAndLastName[1]/g;
			$body =~ s/\[COMPANY\]/$company_name/g;
			$body =~ s/\[OPEN_TICKET_COUNT\]/$openTicketsCount/g;
			$body =~ s/\[CLOSED_TICKET_COUNT\]/$closedTicketCount/g;
			$body =~ s/\[PENDING_TICKET_COUNT\]/$pendingTicketsCount/g;
			$body =~ s/\[PENDING_TICKET_SUBJECTS\]/$pendingTicketSubjects/g;
			$body =~ s/\[CONTRACT_TYPE\]/$contract_type/g;
			$body =~ s/\[CONTRACT_EXPIRATION\]/$contract_exp_date/g;
			$body =~ s/\[USER_LOGIN\]/$login/g;
			$body =~ s/\[PASSWORD\]/$password/g;
			$body =~ s/\[COMPANY_PRODUCTS\]/$productNameString/g;
			if ($verify eq "YES") {
				print "<form name='verify' method = 'post'>
					<input type='hidden' name='filter' value='$filter'>
					<input type='hidden' name='subject' value='$subject'>
					<input type='hidden' name='body' value='$originalBody'>
					<input type='hidden' name='verify' value='NO'>
					<textarea rows='30' cols='100' READONLY>$body</textarea>
					<input type='button' name='back' value='Go Back' onclick='history.back()'>
					<input type='submit' name='submit' value='Send'>
					</form>";
					last;
			} else {
                                sendMail("matt\@iointegration.com", $subject, $body);
                                last;
			}
		};
		if($@)
		{
			print "Could not send to $email\n";
			next;
		}
	}
	$sth->finish();
	$dbh->disconnect();
}

sub filterTutorial()
{
	print header();
	background();
	bodyAndLoad();
	print "<b>Using Filter Expressions</b><p>
	What are Filter Expresssions? <br>
	Filter Expressions allow you to narrow down the user list that you would like to send mails to. You can narrow it down by many attributes including but not limited
	to, product names, contract types, product versions and so on.<p>
	Filter Expression Keywords:<br>
	The keywords you use in the filter specify what you can limit the users by. When using the keywords leave out the quotes.<br>
	\"prod_name\" = Product Name<br>
	\"prod_version\" = Product Version<br>
	\"prod_oper_system\" = The operating system that any of their product run on<br>
	\"contract_type\" = The type of contract they have with IOI. ie \"Gold\",\"Silver\" etc.<br>
	\"contract_date_created\" = The date that the contract was created<br>
	\"contract_date_expired\" = The date that their contract will expire<br>
	\"comp_name\" = Company name<p>
	
	Filter Expression Tutorial:
	Below are some examples of the types of expressions you would put into the filter expression box in order to filter the users you wish to send emails to.<br>
	<br>
	1.)To find all users from the company 'IOI'<br>
	comp_name ISEQUALTO 'IOI'<br>
	2.)To find all users with the product 'FullPress'<br>
	prod_name ISEQUALTO 'fullpress'<br>
	3.)To find all users with the product FullPress or the product FlashNet<br>
	prod_name ISEQUALTO 'fullpress' or prod_name = 'flashnet'<br>
	4.)To find all users with the product FullPress and the contract type of Gold<br>
	prod_name ISEQUALTO 'fullpress' and contract_type ISEQUALTO 'gold'<br>
	5.)To find all contracts that are due to expire by March 12 2007 or sooner<br>
	contract_date_expired <= 2006-03-12 #Note the date must be in this format yyyy-mm-dd<br>";
}