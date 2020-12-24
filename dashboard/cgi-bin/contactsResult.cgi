#!/usr/bin/perl

################################################################################
#
#       File Name: contactsResult.cgi
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
#
################################################################################

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
use CGI;
use DBI;
use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
$REQUIRE_DIR ='c:/Inetpub/scripts/IOIMods';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";

my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 1000000;
$cgi = new CGI;
print $cgi->header();
if (param("sub_name"))
{
	viewTickets();
}

else { contactsResults(); }

sub contactsResults()
{
	#print $cgi->start_html(-title=>'IOI Contacts');
	$search_name = $cgi->param('customer');
	$searchCompany = $cgi->param('company');
	$customer_select = $cgi->param('customer_select');
	$company_select = $cgi->param('company_select');
	
	if ($search_name ne "" and  $company_select ne "" )
        {		
                $statement = "SELECT sub_name, sub_login, sub_comp_link, sub_e_mail, sub_phone, cell_phone
                FROM users
                WHERE sub_name like '%$search_name%' or sub_comp_link = '$company_select' order by sub_comp_link;";
        }
	elsif ($search_name ne "" and $company_select eq "")
	{
		$statement = "SELECT sub_name, sub_login, sub_comp_link, sub_e_mail, sub_phone,cell_phone
			FROM users
			WHERE sub_name like '%$search_name%' order by sub_comp_link";
	}
	elsif ($customer_select ne "" and $company_select ne "")
	{
			$statement = "SELECT sub_name, sub_login, sub_comp_link, sub_e_mail, sub_phone, cell_phone
			FROM users
			WHERE sub_name like '%$customer_select%' or sub_comp_link = '$company_select' order by sub_comp_link;";
	}
	elsif ($customer_select ne "" and $company_select eq "")
	{
		
		$statement = "SELECT sub_name, sub_login, sub_comp_link, sub_e_mail, sub_phone, cell_phone
			FROM users
			WHERE sub_name = '$customer_select' order by sub_comp_link";
	}
	elsif ($company_select ne "")
	{
			$statement = "SELECT sub_name, sub_login, sub_comp_link, sub_e_mail, sub_phone,cell_phone
			FROM users
			WHERE  sub_comp_link = '$company_select' order by sub_comp_link;";	
	}
	elsif ($customer_select ne "")
	{
		$statement = "SELECT sub_name, sub_login, sub_comp_link, sub_e_mail, sub_phone,cell_phone
			FROM users
			WHERE sub_name = '$customer_select' order by sub_comp_link";
	}
	else 
	{
		$statement = "Select sub_name, sub_login, sub_comp_link, sub_e_mail, sub_phone,cell_phone
			FROM users order by sub_comp_link";
	}
	headers('IOI Contacts');
	bodyAndLoad();
	background();
	tableHead('95%');
	print"
	  <tr><td><b>Name</b></td><td><b>Phone #</b></td><td><b>Cell #</b></td><td><b>Email</b></td><td><b>Company</b></td><td><b>Billing Address</b></td><td><b>Serial #</b></td></tr>";
	  $sth = $dbh->prepare($statement);
	  $sth->execute();
		while(($sub_name, $sub_login, $sub_comp_link, $sub_e_mail, $sub_phone, $cell_phone) = $sth->fetchrow_array)
		{
			$comp = $dbh->prepare("SELECT comp_name, comp_bill_address, comp_bill_city, comp_bill_state, comp_bill_zip FROM company WHERE comp_case_num = '$sub_comp_link'");
			$comp->execute();
			($comp_name, $comp_bill_address, $comp_bill_city, $comp_bill_state, $comp_bill_zip) = $comp->fetchrow_array();
			$statement = "SELECT prod_name, prod_part_num FROM product WHERE prod_comp_link = '$sub_comp_link' AND prod_part_num <> ''";
			$serial = $dbh->prepare($statement);
			$serial->execute();
	
		
			print "<tr  bgcolor='#B0B0B0'><td><a href='contactsResult.cgi?sub_name=$sub_login&comp_name=$comp_name'> $sub_name</a></td><td>$sub_phone</td><td>$cell_phone</td><td>$sub_e_mail</td>
			<td>$comp_name</td><td>$comp_bill_address $comp_bill_city $comp_bill_state $comp_bill_zip</td><td>";
					while(@serial = $serial->fetchrow_array())
			{
				print "@serial &nbsp;&nbsp;";
			}
			print"</td></tr>";
		}
	print "</table>";
	end_html();
}
sub viewTickets()
{
	$sub_name = param('sub_name');
	$comp_name = param('comp_name');
	$PAGE_TITLE = 'View Tickets';
	header('View Tickets');
	background();
	print "<center><font color ='#808080'>Active tickets for $comp_name</font></center>\n";
	tableHead('95%');
	print "<tr><td>Case Number</td><td>Submitted By</td><td>Subject</td><td>Product</td><td>Serial Number</td><td>Assigned To</td><td>Last Modified</td></tr>";
	$sth = $dbh->prepare("SELECT status, short_desc, assigned_to, date_mod, time_mod, case_num, submitted_by, prob_prod_link FROM problems WHERE prob_comp_link = (SELECT DISTINCT sub_comp_link FROM users WHERE sub_login = '$sub_name') AND status <> 'Closed' AND status <> 'Awaiting Bug Fix' AND status <> 'Awaiting Feature Request'");
	$sth->execute();
	while(($status, $short_desc, $assigned_to, $date_mod, $time_mod, $case_num, $submitted_by, $prob_prod_link) = $sth->fetchrow_array())
	{
		$check = 1;
		$user = $dbh->prepare("SELECT sub_name, sub_e_mail, sub_phone FROM users WHERE sub_login = '$submitted_by'");
		$user->execute();
		($user_name,$sub_email,$sub_phone) = $user->fetchrow_array();
		$product = $dbh->prepare("SELECT prod_name, prod_part_num FROM product WHERE prod_case_num = '$prob_prod_link'");
		$product->execute();
		($prod_name,$prod_part_num) = $product->fetchrow_array();
		$user->finish();
		$date_mod =~ s/00:00:00//g;
		push @contactsRow, "<tr><td><a href='respondTicket.cgi?case_num=$case_num&viewTicket=true'>$case_num</a></td><td>$user_name</td><td>$short_desc</td><td>$prod_name</td><td>$prod_part_num</td><td>$assigned_to</td><td>$date_mod $time_mod</td></tr>\n";
	}

	push @contactsRow,"</table>";
	print @contactsRow;
		if ($check != 1)
	{
		print "<center><font color = '#808080'>No Active Tickets for this user.</center>";
	}
	end_html();
}

	
#print $cgi->end_html();		