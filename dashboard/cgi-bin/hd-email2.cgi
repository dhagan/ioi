#!/usr/bin/perl

################################################################################
#
#       File Name: email2.cgi
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
#       01/26/2007      B. Scarborough  Modified to allow for new field cust_problem in DB
#       01/30/2007      B. Scarborough  Modified printEmailBoxes() to allow for company tech email
#       02/09/2007      B. Scarborough  Modified to allow for redirect to helpdesk
#       03/29/2007      B. Scarborough  Modified to allow for non-tech check on update
#       06/01/2007      B. Scarborough  Modified many HTML field names to comply with new SubmitMail.cgi
#       08/10/2007      B. Scarborough  Modified to support apostrophes in email addresses
#       08/10/2007      B. Scarborough  Modified printEmailBoxes() to get correct company tech email address
################################################################################

use CGI;
use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
use threads;
use File::Find::Rule;
use Time::Format qw(time_format %time);
use DBI;

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";

$time{$format};
$cgi = new CGI;
my $dbh = getDBConnection();
$dbh->{'LongReadLen'} = 1000000;

$case_num = $cgi->param('case_num');
$email_action = $cgi->param('email_action');
$link = $cgi->param('link');
$user = $cgi->param('user');
$assigned_to = $cgi->param('assigned_to');
$status = $cgi->param('status');
$priority = $cgi->param('priority');
$xinet_ticket_num = $cgi->param('xinet_ticket_num');
$time_spent = $cgi->param('time_spent');
$subject = $cgi->param('subject');
$bug_ticket_num = param('bug_ticket_num');
$product = $cgi->param('product');
$problem = $cgi->param('problem');
$comp_case_num = $cgi->param('comp_case_num');
$customer = $cgi->param('submitted_by');
$newTicket = $cgi->param('newticket');
$assigned_to = $cgi->param('assigned_to');
$attachment1 = $cgi->param('attachment1');
$attachment2 = $cgi->param('attachment2');
$attachment3 = $cgi->param('attachment3');
$submit_time = $time{"hh:mm:ss"};
$date = time_format('yyyy/mm/dd');
$rows = 0;


($sub_e_mail, $sub_name, $sub_comp_link) = &getUserSession();
if (!$sub_e_mail || !$sub_name || !$sub_comp_link) {
   print $cgi->header();
   print "You appear to be logged out, please login";
   print "<input id='login' type='button' value='Login' onclick=\"window.location='hd-login.cgi'\"/>";
   exit;
}


#######################################Submit Ticket###########################################
$sth = $dbh->prepare("SELECT allow_submit,submitted_by FROM problems WHERE case_num = '$case_num'");
$sth->execute();


my ($allow_submit, $submitted_by) = $sth->fetchrow_array();
if ($newTicket eq "true")
{
	$allow_submit = 1;
}
if ($allow_submit == 1)
{
    nonTechCheck($user, $case_num, $subject, $submit_time, $date, $assigned_to);
	
### DJH 12/27/2020 
###  re-purpose this block and more for create and update
###
	$status = 'Pending IOI';
	#If this is a new ticket
	if ($newTicket eq "true" and $case_num eq "")
	{	
		$case_num = getCaseNumber();
		$subject = $dbh->quote($subject);
		$date = $dbh->quote($date);
		$submit_time = $dbh->quote($submit_time);
		$product = $dbh->quote($product);
		$comp_case_num = $dbh->quote($comp_case_num);
		$customer = $dbh->quote($customer);
		$assigned_to = $dbh->quote($assigned_to);
		$time_spent = $dbh->quote($time_spent);
		$priority = $dbh->quote($priority);
		$bug_ticket_num = $dbh->quote($bug_ticket_num);
		$statement = "INSERT INTO problems (case_num,status,short_desc,priority_type,assigned_to,time_spent,date_open,date_mod,time_mod,prob_prod_link,prob_comp_link,submitted_by,xinet_ticket_num,bug_ticket_num) values
		('$case_num','$status', $subject,$priority,$assigned_to,$time_spent,$date,$date,$submit_time,$product,$comp_case_num,$customer,'$xinet_ticket_num',$bug_ticket_num)";
		$sth = $dbh->prepare($statement);
		$sth->execute();
                $sth = $dbh->prepare("SELECT id FROM problems WHERE case_num = '$case_num'");
                $sth->execute();
                my $problem_id = $sth->fetchrow_array();
                $description = $dbh->quote($problem);
                my $description_updated_by = $dbh->quote("$sub_name");
                my $action = "Updated by $sub_name";
                my $is_customer = false;
                my $statement = "INSERT INTO `descriptions` (problem_id, description, status, created, description_updated_by, action, is_customer) VALUES ('$problem_id', $description, '$status', NOW(), $description_updated_by, '$action', '$is_customer')";
                $sth = $dbh->prepare($statement);
		$sth->execute();
		$dbh->commit();
		
	#If an existing ticket
	} elsif ($case_num ne "") {
		$subject = $dbh->quote($subject);
		$statement = "UPDATE problems SET date_mod = '$date', time_mod = '$submit_time', status='$status' WHERE case_num = '$case_num'";
                $sth = $dbh->prepare($statement) or die print $dbh->errstr;
		$sth->execute() or die print $dbh->errstr;
                $sth = $dbh->prepare("SELECT id FROM problems WHERE case_num = '$case_num'");
                $sth->execute();
                my $problem_id = $sth->fetchrow_array();
                $description = $dbh->quote($problem);
                my $description_updated_by = $sub_name . "<" . $sub_e_mail . ">";
                my $action = "Updated by $sub_name";
                my $is_customer = true;
                my $statement = "INSERT INTO `descriptions` (problem_id, description, status, created, description_updated_by, action, is_customer) VALUES ('$problem_id', $description, '$status', NOW(), '$description_updated_by', '$action', '$is_customer')";
                $sth = $dbh->prepare($statement);
		$sth->execute();
		$dbh->commit() or die print $dbh->errstr;
	}
	$sth = $dbh->prepare("UPDATE problems SET allow_submit = 0 WHERE case_num = '$case_num'");
	$sth->execute();
	$dbh->commit();
	if ($attachment1 ne ""){attachmentUpload("attachment1");}
	if ($attachment2 ne ""){attachmentUpload("attachment2");}
	if ($attachment3 ne ""){attachmentUpload("attachment3");}

}

$is_customer = $email_action eq "Email Client";

############################################Email#################################################
@remote_user = split(/ /,$user);

use File::Find::Rule;
my @files = File::Find::Rule->file()
							->name('*')
							->in("/Library/WebServer/dashboard/attachments/$case_num");

################
$sth = $dbh->prepare("SELECT xinet_ticket_num,supplier_email,customer_email,submitted_by,prob_prod_link,assigned_to,xinet_ticket_num,short_desc, status, prob_prod_link, prob_comp_link FROM problems WHERE case_num ='$case_num'");

$sth->execute();
($xinet_ticket_num,$supplier_email,$customer_email,$submitted_by,$prob_prod_link,$assigned_to,$supplier_serial_num,$short_desc,$status,$prob_prod_link,$prob_comp_link)=$sth->fetchrow_array();
@supplier_emails = split(" ",$supplier_email);
@customer_emails = split(" ",$customer_email);
$sth = $dbh->prepare("SELECT sa_name,sa_email_header,sa_email_signature FROM staff WHERE sa_login = '$user'");
$sth->execute();
($staff_name,$staff_greeting,$staff_signature) = $sth->fetchrow_array();
$sth = $dbh->prepare("SELECT sub_name,sub_e_mail FROM users WHERE sub_login = '$submitted_by'");
$sth->execute();
($cust_name,$cust_email) = $sth->fetchrow_array();
$sth = $dbh->prepare("SELECT prod_name,prod_part_num FROM product WHERE prod_case_num = '$prob_prod_link'");
$sth->execute();
($product,$prod_part_num) = $sth->fetchrow_array();
$sth = $dbh->prepare("SELECT comp_name FROM company WHERE comp_case_num = '$prob_comp_link'");
$sth->execute();
$comp_name = $sth->fetchrow_array();
@Name = split(/ /,$cust_name);
$staff_greeting =~ s/{customer_name}/@Name[0]/gs;
if($staff_greeting eq "")
{
	$staff_greeting = "Hello @Name[0],"
}
if($staff_signature eq "")
{
	$staff_signature = "Thanks,

@remote_user[0]

IOI Support";
}

### DJH 10/23/2011 added logic to read from the vendor table
$sth = $dbh->prepare("SELECT v.name, v.email, v.include_prefix, v.prefix, v.include_vendor_ticket_number FROM vendor v LEFT JOIN product_vendor_relationship pv ON pv.vendor_name = v.name JOIN product p ON pv.product_name = p.prod_name WHERE p.prod_case_num = '". $prob_prod_link . "'");
$sth->execute();
($supplier,$supplier_email, $include_prefix, $prefix, $include_vendor_ticket_number) = $sth->fetchrow_array();

if ( $supplier eq ""){
	$supplier = "No Supplier Information available";
	$supplier_email = "";
}

if ($assigned_to eq "nobody" or $email_action eq "Submit")
{
	#print "<center><p><a href = 'respondTicket.cgi?case_num=$case_num&user=$user'>Click Here to Modify Your Recently Updated Ticket</a></p></center>";
        print $cgi->redirect("helpdesk.cgi?modified=$case_num");
        ### DJH print $cgi->redirect("/dashboard/thankYou.cgi?modified=$case_num");
}
else 
{
        print $cgi->header();
        print $cgi->start_html(-title=>'Helpdesk Email' );
        print "<style type='text/css'>
        	<!--
        	body {
        	background-color: #C0C0C0;
        	}
        	-->
        	</style>";
        if($email_action eq "Email Client" )
        {
            print"<style type='text/css'>
                <!--
                .style4 {font-size: 12px}
                body,td,th {
                        font-size: 12px;
                }
                -->
                </style>";
            print"<center>
            <b>HelpDesk Email</b>
            <table width = '95%' border='1' cellspacing='0' cellpadding='0' bgcolor='#909090'>
            <form ENCTYPE='multipart/form-data' id='FormName' name='FormName' action='SubmitMail.cgi' method='post'>
            <input type='hidden' name='user' value='$user'>
            <input type = 'hidden' name = 'case_num' value = '$case_num'>
            <input type = 'hidden' name = 'remote_user' value = '@remote_user[0]'>
            <input type=\"hidden\" name=\"to\" id=\"email\" VALUE=\"$cust_email\">
            <input type='hidden' name='email_type' value='customer'>
            <input type='hidden' name='donotsend' value='false'>
            <input type='hidden' name='assigned_to' VALUE = '$assigned_to'>";
            $comp_case_num =~ s/'//g;
            print "<tr bgcolor='#B0B0B0'><td colspan='2'><div align='center'><font size='4px'>This email will be sent to $cust_name</font></div></td></tr>
            <tr><td><div align='center'>CC:</div></td><td ><div id='cc_div' align='center'><input size='50' type='text' id='cc' name='cc' /><br />";
            printEmailBoxes("customer");
            print "</div></td></tr>
            <tr><td><div align='center'>BCC:</div></td><td ><div id='bcc_div' align='center'><input size='50' type='text' style='width:350' id='bcc' name='bcc'><br /></div></td></tr>
            <tr><td align='center' colSpan='2'><input type='button' value='Add Email Addresses' onClick='window.open(\"addresses.cgi?email_type=customer&comp_case_num=$comp_case_num\", \"addressWindow\", \"toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=600, height=400, copyhistory=no\")' /></td></tr>";
            printHeader();
            print "</tr><tr>";
            printIntro("customer_greeting");
            print "
            </tr><tr><td colspan = '2'><div align='center'><textarea name='problem' rows='17' cols='98' readonly>";
            
                print "$problem";
                printBodyHead();
            if ($status eq "Closed")
            {
                print "\n\nThis ticket is now closed. If you wish to reopen the ticket please respond to this email or call IOI tech support. \n";
            }
            
            print "</textarea></div></td></tr>";
            print "<tr>";
            printSignature();
        }
        if ($email_action eq "Email Vendor")
        {
            print"
            <center>
            <b>HelpDesk Email</b>
            <table width = '95%' border='1' cellspacing='0' cellpadding='0' bgcolor='#909090'>
            <div align='center'>
            <form ENCTYPE='multipart/form-data' id='FormName' name='FormName' action='SubmitMail.cgi' method='post'>
            <input type='hidden' name='user' value='$user'>
            <input type = 'hidden' name = 'case_num' value = '$case_num'>
            <input type=\"hidden\" name=\"to\" id=\"email\" VALUE =\"$supplier_email\">
            <input type='hidden' name='email_type' value='supplier'>
            <input type = 'hidden' name = 'remote_user' value = '@remote_user[0]'>
            <input type='hidden' name='donotsend' value='false'>
            <input type='hidden' name='assigned_to' VALUE = '$assigned_to'>
            <\p>"; 
            print "<tr bgcolor='#B0B0B0'><td colspan='2'><div align='center'><font size='4px'>This email will be sent to $supplier</font></td></tr>
            <tr><td><div align='center'>CC:</div></td><td><div id='cc_div' align='center'><input type='text' size='50' id='cc' name='cc'><br />";
            printEmailBoxes("supplier");
            print "</div></td></tr>
            <tr><td><div align='center'>BCC:</div></td><td ><div id='bcc_div' align='center'><input type='text' size ='50' id='bcc' name='bcc'><br /></div></td></tr>
            <tr><td align='center' colSpan='2'><input type='button' value='Add Email Addresses' onClick='window.open(\"addresses.cgi?email_type=supplier&comp_case_num=$comp_case_num\", \"addressWindow\", \"toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=600, height=400, copyhistory=no\")' /></td></tr>
            ";
            printHeader('ticket');
            print"</tr><tr>";
            printIntro("supplier_greeting");
            print"
            </tr><tr><td colspan='2'><div align='center'><textarea name='problem' rows='17' cols='98' readonly>";
            print "Customer: $cust_name
            Company: $comp_name\n";
            
            if ($supplier eq "Xinet")
            {
             print "Xinet Serial # $prod_part_num
            ";
            }
            print "\n";
            print "$problem 
            
            ";
            printBodyHead();
            if ($status eq "Closed")
            {
                print "This ticket is now closed. If you wish to reopen the ticket please respond to this email or call IOI tech support. \n";
            }
            print "
            </textarea></div></td></tr><tr>";
            printSignature();
        }
        if ($email_action eq "Email")
        {
            print"
            <center>
            <b>HelpDesk Email</b>
            <table width = '95%' border='1' cellspacing='0' cellpadding='0' bgcolor='#909090'>
            <div align='center'>
            <form ENCTYPE='multipart/form-data' id='FormName' name='FormName' action='SubmitMail.cgi' method='post'>
            <input type='hidden' name='user' value='$user'>
            <input type = 'hidden' name = 'case_num' value = '$case_num'>
            <input type='hidden' name='email_type' value='internal'>
            <input type = 'hidden' name = 'remote_user' value = '@remote_user[0]'>
            <input type='hidden' name='donotsend' value='false'>
            <input type='hidden' name='assigned_to' VALUE = '$assigned_to'>
            <\p>"; 
            print "<tr bgcolor='#B0B0B0'><td colspan='2'><div align='center'><font size='4px'>This email will be sent to IO Employees</font></td></tr>
            <tr><td><div align='center'>TO:</div></td><td><div id='to_div' align='center'><input type='text' size='50' id='email' name='to'><br /></div></td></tr>
            <tr><td><div align='center'>CC:</div></td><td><div id='cc_div' align='center'><input type='text' size='50' id='cc' name='cc'><br /></div></td></tr>
            <tr><td><div align='center'>BCC:</div></td><td ><div id='bcc_div' align='center'><input type='text' size='50' id='bcc' name='bcc'><br /></div></td></tr>
            <tr><td align='center' colSpan='2'><input type='button' value='Add Email Addresses' onClick='window.open(\"addresses.cgi?email_type=tech&comp_case_num=$comp_case_num\", \"addressWindow\", \"toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, resizable=yes, width=600, height=400, copyhistory=no\")' /></td></tr>
            ";
            printHeader('ticket');
            print"</tr><tr>";
            printIntro("supplier_greeting");
            print"
            </tr><tr><td colspan='2'><div align='center'><textarea name='problem' rows='17' cols='98' readonly>";
            print "Customer: $cust_name
            Company: $comp_name\n";
            
            if ($supplier eq "Xinet")
            {
             print "Xinet Serial # $prod_part_num
            ";
            }
            print "\n";
            print "$problem 
            
            ";
            printBodyHead();
            if ($status eq "Closed")
            {
                print "This ticket is now closed. If you wish to reopen the ticket please respond to this email or call IOI tech support. \n";
            }
            print "
            </textarea></div></td></tr><tr>";
            printSignature();
        }
        print "</tr></div>";
        
        print "	<script language='JavaScript'>
                function updateEmail(value)
                {
                        
                        document.formname.cc_supplier.value = value;
                }
        
        </script>";
        print "<tr>";
        printAttachments();
        $problem =~ s/"/'/g;
        print "</tr></table>";
        print "<script language='javascript'>
                        function fillNames()
                        {
                                appendNames('to_boxes', 'email');
                                appendNames('cc_boxes', 'cc');
                                appendNames('bcc_boxes', 'bcc');
                        }
                        function appendNames(src, dest)
                        {
                                var temp = document.getElementsByName(src);
                                var email = document.getElementById(dest);
                                if((email.value != '') && (temp.length != 0)) {
                                        email.value = email.value + ', ';
                                }
                                for(var i = 0; i < temp.length; i++) {
                                        if(temp[i].checked)
                                        {
                                                email.value = email.value + temp[i].value + ', ';
                                        }
                                }
                                if(email.value.lastIndexOf(',') == (email.value.length - 2)) {
                                        email.value = email.value.substr(0, email.value.length - 2);
                                }
                        }
               </script>";
        print "<center><input type='submit' name='Send Mail' onClick='fillNames()' value = 'Submit Mail'><input type='submit' name='Do Not Send Mail' value='Do Not Send Mail' onClick=\"document.FormName.donotsend.value = 'true' \"></form>
        <p><strong>If you have found an error in your email, please click 
        
        <form name='form2' action='respondTicket.cgi' method='post'>
        <input type='hidden' value= \"$problem\" name='problem'><input type='hidden' name='case_num' value='$case_num'> <input type='hidden' name='user' value='$user'><input type='submit' name='submit' value='Fix Mistake'></form>
        and make the changes needed.</strong></center>
        ";
}

print $cgi->end_html();
#   Disconnect.
$sth->finish();
$dbh->commit();
$dbh->disconnect();
sub printHeader
{
	$ticket = $_[0];
	if ($ticket ne "" and $supplier eq "Xinet")
	{
		$ticket = "Ticket :$supplier_serial_num";
	}
	elsif ($ticket ne "" and $supplier eq "Dalim")
	{
		$ticket = $supplier_serial_num;
	}
	else { $ticket = ""};
	if ($supplier eq "Xinet")
	{
		if ($supplier_serial_num ne "")
		{
		print "<td><div align='center'>Subject:</div> </td><td> <div align='center'><input type='text' name='subject' size ='50' MAXLENGTH='200' value=\"$ticket '$case_num' $short_desc\" READONLY></div></td>";
		}
		else 
		{
		print "<td><div align='center'>Subject:</div></td><td> <div align='center'><input type='text' name='subject' size ='50' MAXLENGTH='200' value=\"'$case_num' $short_desc\" READONLY></div></td>";
		}
	}
	elsif ($supplier eq "Dalim")
	{
		if ($supplier_serial_num ne "" and $status eq "Pending Vendor")
		{
			print "<td><div align='center'>Subject: </div></td><td><div align='center'> <input type='text' name='subject' size ='50' MAXLENGTH='200' value=\" '$case_num' $short_desc  \'$ticket\' \" READONLY></div></td>";
		}
		else
		{
			print "<td><div align='center'>Subject:</div> </td><td><div align='center'> <input type='text' name='subject' size ='50' MAXLENGTH='200' value=\"'$case_num' $short_desc \" READONLY></div></td>";
		}
	}
	else 
	{
		$email_subject = "";
		if ($supplier_serial_num ne "" and $include_prefix eq "1") {
			$email_subject = $prefix;
		}

		if ($supplier_serial_num ne "" and $include_vendor_ticket_number eq "1") {
			$email_subject = $email_subject . " " . $supplier_serial_num;
		}

		$email_subject = $email_subject . " '$case_num' $short_desc";

		print "<td><div align='center'>Subject:</div> </td><td> <div align='center'><input type='text' name='subject' size ='50' MAXLENGTH='200' value=\"'$email_subject \" READONLY></div></td>";
	}  
}
sub printAttachments
{
	if ($email_action eq "Email Vendor" or $email_action eq "Email Client" or $email_action eq "Email")
	{
	print "<td><div align='center'><b><font size='2'>This tickets attachments<br />(Check to send with email):</div></td><td><div align='center'>";
	}
	else
	{
		print "<td colspan = '2'><div align='center'><b><font size='2'>This tickets attachments (Check to send with email):</div></td><td colspan = '2'><p><div align='center'>";
	}
	$total_files = 0;
	foreach $file(@files)
	{
		if ($file =~ /$case_num\//)
		{
			$filename = $';
		}
		print "<input type ='checkbox' name='ticketAttachment' value='$file'>$filename &nbsp;&nbsp;&nbsp;&nbsp;";
	}
	print "</font></b></div></td>"; 
}
sub printSignature
{
	print "<td colspan='2'><div align='center'><textarea id='signature' name = 'signature' rows = '6' cols = '98'>
$staff_signature
</textarea><p></div></td>";
}
sub printIntro
{
	my $greeting = $_[0];
	if ($greeting eq "supplier_greeting")
	{
	print "<td><div align='center'>Greeting:</div></td><td><div align='center'> <input type = 'text' id='greeting' size = '50' name = 'greeting' value = ''><input type='button' value='Edit Preferences' onClick='window.open(\"preferences2.cgi?user=$user&customer_name=@Name[0]\", \"preferencesWindow\", \"toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, width=500, height=450, copyhistory=no\")' /></div></td>
	</center>";
	}
	else {
	print "<td><div align='center'>Greeting: </div></td><td><div align='center'><input type = 'text' id='greeting' size = '50' name = 'greeting' value = '$staff_greeting'><input type='button' value='Edit Preferences' onClick='window.open(\"preferences2.cgi?user=$user&customer_name=@Name[0]\", \"preferencesWindow\", \"toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, width=500, height=450, copyhistory=no\")' /></div></td>";
	}
}
sub printBodyHead
{
	if ($status eq "Awaiting Feature Request")
	{
		print "This ticket is now awaiting a feature request. \n \n";
	}
	if ($status eq "Awaiting Bug Fix")
	{
		print "This ticket is now awaiting a bug fix. \n \n";
	}
}
sub upload
{
	my $file =@_[0];
	#use CGI::Upload;
	$query = new CGI;
	$upload_directory = "/Library/WebServer/dashboard/uploads";
	#mkdir ($upload_directory) or die "Cannot Make directory";
	
	if (mkdir ($upload_directory))
	{	
		chmod(0755,$upload_directory);
		my $fh=param($file);
		$newfh = $fh;
		$newfh =~ s/ /_/g;
		
		open UPLOADFILE, ">$upload_directory\\$newfh";
		binmode UPLOADFILE; 
		while ( <$fh> ) 
		{ 
		print UPLOADFILE; 
		} 
		close UPLOADFILE;
	}
	else {
		#print "Cannot Make Directory $! (errno)"; 
		chmod(0755,$upload_directory);
		my $fh=param($file);
		$newfh = $fh;
		$newfh =~ s/ /_/g;
		
		open UPLOADFILE, ">$upload_directory\\$newfh";
		binmode UPLOADFILE; 
		while ( <$fh> ) 
		{ 
		print UPLOADFILE; 
		} 
		close UPLOADFILE;
	
	}
}

# Function: printEmailBoxes
# Purpose: Displays checkboxes for the email page.
# Inputs: type('customer' or 'support')
# Returns: None

sub printEmailBoxes
{
        my $type = $_[0];
        
        # Displays company's email address and company's tech email address if they exist, default is checked
        if($type eq "customer")
        {
            my $company_email = selectValues("SELECT comp_email FROM company WHERE comp_case_num = '$comp_case_num'");
	        print "<input type='checkbox' name='cc_boxes' value='$company_email' checked><b>Company Email</b>" if ($company_email ne "");
            my $company_tech_email = selectValues("SELECT staff.sa_e_mail FROM staff, company WHERE company.comp_case_num = '$comp_case_num' AND company.comp_tech = staff.sa_login");
	        print "<input type='checkbox' name='cc_boxes' value='$company_tech_email' checked><b>Company Tech</b>" if ($company_tech_email ne "");
            print "<br />" if ($company_email ne "" or $copmany_tech_email ne "");
        }
        
        # Gets list of previoiusly sent to email addresses
        (my $old_email_string)=selectValues("SELECT $type" . "_email FROM problems WHERE case_num = '$case_num'");
        my @old_emails = split(" ",$old_email_string);
	foreach $email(@old_emails)
	{
		if (($email ne $cust_email) and ($email ne $company_email) and !($email =~ />/))
  		{
  			print "<input type = \"checkbox\" name=\"cc_boxes\" value=\"$email\" checked>$email ";
	  	}	
	}
	print "</td></tr>";
}

# Function: nonTechCheck
# Purpose: Check to see if a non-tech is updating, If so email assigned tech or all techs if necessary
# Inputs: user(username), case_num(case number of ticket being updated), subject(of problem), problem(most recently stated)
#         timestamp(time + date), assigned_to(tech the ticket is assigned to)
# Returns: None

sub nonTechCheck
{
        my $user = $_[0];
        my $case_num = $_[1];
        my $subject = $_[2];
        my $timestamp = $_[3] . " " . $_[4];
        my $assigned_to = $_[5];

        my $problem = get_ticket_descriptions( $case_num, false);
        
       	$sth = $dbh->prepare("SELECT sa_login FROM staff WHERE (sa_login = '$user' OR sa_e_mail = '$user') AND sa_dept <> 'IT'");
        $sth->execute();


        #If update is by a non-tech
        if($sth->fetchrow_array()) {
                my $assigned;
                my $email;
                my $body;
                my $email_subject = "Ticket # $case_num has been updated by $user";
                
                #If tech is available notify that tech, otherwise notify all other techs
                if(checkTechStatus($assigned_to) eq "available") {
                        $sth = $dbh->prepare("SELECT sa_e_mail FROM staff WHERE sa_login = (SELECT assigned_to FROM problems WHERE case_num = '$case_num')");
                        $sth->execute();
                        ($email) = $sth->fetchrow_array();
                        $body = "Ticket $case_num has been updated by $user. Please log onto the helpdesk to see what action is required\n\nTime Sent: $timestamp\n\nSubject: $subject \n\n Problem: $problem\n\n To update this ticket please go to http://dashboard.iointegration.com/cgi-bin/respondTicket.cgi?case_num=$case_num&user=$assigned";
			sendMail($email,$email_subject,$body);
                } else {
                        $sth = $dbh->prepare("SELECT sa_login,sa_e_mail FROM staff WHERE sa_dept = 'IT' AND sa_access = 'Active'");
			$sth->execute();
			while ((my $sa_login, $email) = $sth->fetchrow_array())
			{
				$body = "This ticket is assigned to $assigned_to, who is unavailable right now. Please determine if this ticket requires attention.\n\n" .
                                        "Ticket $case_num has been updated by $user. Please log onto the helpdesk to see what action is required\n\nTime Sent: $timestamp\n\nSubject: $subject \n\n Problem: $problem\n\n To update this ticket please go to http://dashboard.iointegration.com/cgi-bin/respondTicket.cgi?case_num=$case_num&user=$sa_login";
				sendMail($email,$email_subject,$body);
			}
                }
        }
}

sub get_ticket_descriptions {
    my $case_num = $_[0];
    my $is_customer = $_[1];
    my $query = "SELECT d.description, d.description_updated_by, d.status, d.action, d.created FROM descriptions d JOIN problems p ON p.id = d.problem_id WHERE p.case_num = '$case_num' ORDER BY d.created DESC";
    if ($is_customer) {
	$query = "SELECT d.description, d.description_updated_by, d.status, d.action, d.created FROM descriptions d JOIN problems p ON p.id = d.problem_id WHERE p.case_num = '$case_num' AND d.is_customer = '1' ORDER BY d.created DESC";
    }
    $sth = $dbh->prepare($query);
    $sth->execute();
    my $return = '';
    while ((my $description, my $description_updated_by, my $status, my $action, my $created) = $sth->fetchrow_array())
    {
         $return .= $description . "\n\n";
	##  [- Awaiting Feature Request - 08:55:05 2005/12/29 - Liz - Ticket updated by Liz -] 
	$return .= '[- '  . $status . ' - ' . $created . ' - ' .  $description_updated_by . ' - ' .  $action . ' -]'. "\n\n"
    }  
    return $return;
}
