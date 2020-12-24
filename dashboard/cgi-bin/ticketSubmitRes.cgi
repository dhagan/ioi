#!/usr/bin/perl

################################################################################
#
#       File Name: ticketSubmitRes.cgi
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
#       03/29/2007      B. Scarborough  Modified to allow for generic sendMail function
################################################################################

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
use CGI;
use DBI;
use Time::Format qw(time_format %time);
$time{$format};
$submit_time = $time{"hh:mm:ss"};
$date=time_format('yyyy/mm/dd');
$cgi = new CGI;
print $cgi->header();
print $cgi->start_html();
print "<style type='text/css'>
<!--
body {
	background-color: #C0C0C0;
}
.style1 {color: #909090}

-->
</style>";
my $dbh = getDBConnection();
$newCompany = $cgi->param('newCompany');
$newCustomer = $cgi->param('newCustomer');
$prod_case_num = $cgi->param('prod_case_num');
$submitted_by = $cgi->param('submitted_by');
$problem = $cgi->param('problem');
$subject = $cgi->param('subject');
$inputBy = $cgi->param('inputBy');
$statement = "select sa_name from staff where sa_e_mail = '$inputBy'";

$sth = $dbh->prepare($statement);
$sth->execute();
$sa_name = $sth->fetchrow_array();
$name = $cgi->param('name');
$company = $cgi->param('company');
$comp_name = $cgi->param('comp_name');
$comp_case_num = $cgi->param('comp_case_num');
$phone = $cgi->param('phone');
$prob_comp_link = $cgi->param('prob_comp_link');
if ($newCompany eq "" and $newCustomer eq "")
{


	$sth=$dbh->prepare("Select max(id_num) from problem");
		$sth->execute();
		while ( @row = $sth->fetchrow_array ) 
		 {
			$id_num = "@row";
		  }
		$id_num += 1;
$case_num = getCaseNumber();

$email_problem = $problem;
$problem = $problem . "\n[-Opened by $inputBy- $submit_time $date - $name - Open -] \n";
$submit_problem = $dbh->quote($problem);
$submit_subject = $dbh->quote($subject);
$statement = "Insert into problem(status,submitted_by,date_open,date_mod,id_num,case_num,category,problem,short_desc,assigned_to,prob_prod_link,prob_comp_link,time_mod) Values ('Open','$submitted_by','$date','$date',$id_num,'$case_num','TBD',$submit_problem,$submit_subject,'nobody','$prod_case_num','$prob_comp_link','$submit_time')";
$sth=$dbh->prepare($statement) or die print LOG ("Error updating database");
$sth->execute or die print LOG ("Error updating database");
$dbh->commit or die print LOG ("Error updating database");
print "<span class='style1'><center><h3>This ticket has been created in the Helpdesk for $name, your ticket number is $case_num</h3><p>Click <a href='CustomerLookup.cgi'>here<a> to return to the search page.<center></span>";
 $subject_header = "A new ticket, $case_num, has been submitted by $name ($comp_name)";
 
 $sth = $dbh->prepare("select sa_login,sa_e_mail from staff where sa_access <> 'Disabled' and sa_dept = 'IT'");
 $sth->execute();
 while(($sa_login,$sa_email)= $sth->fetchrow_array())
 {

 $email_body = "Ticket $case_num, $subject, has been opened for $comp_name by $name. Please log onto the helpdesk to see what action is required\n
Subject: $subject 

Phone: $phone

Problem: $email_problem\n\nThis message was taken by $sa_name. To update this ticket go to http://dashboard.iointegration.com/cgi-bin/respondTicket.cgi?case_num=$case_num&user=$sa_login&staffmember=$inputBy.";
 sendMail($sa_email, $subject_header, $email_body);
 }
}

else
{
	 if ($newCustomer ne "")
	 {
	 $subject_header = "A new customer, $name, has submitted a ticket for $company";
	 $email_body = "$name is not currently in the database, please add them in order to respond to this problem. \n
Phone: $phone 
	 
Company: $company
	 
Subject: $subject
	 
Problem: $problem
	 
This message was taken by $sa_name, Please do not reply to this email to update the ticket.";
         sendMail("support\@iointegration.com", $subject_header, $email_body);
	  print "<center><h3>This ticket has been sent to IOI support. Click <a href='CustomerLookup.cgi'>here<a> to return to the search page.<center>";
	 }
	 else{
	  $subject_header = "A new customer, $name, has submitted a ticket for a new company $company";
	 $email_body = "$name and company $company is not currently in the database, please add them in order to respond to this problem.\n
Phone: $phone 
	
Company: $company
	 
Subject: $subject
	 
Problem: $problem
	 
	This message was taken by $sa_name, Please do not reply to this email to update the ticket.";
	 sendMail("support\@iointegration.com", $subject_header, $email_body);
         print "<center><h3>
<span class='style1'>This ticket has been sent to IOI support. Click <a href='CustomerLookup.cgi'>here</a> to return to the search page.
<center>
</span>";
	
	 
	 }
 }
print $cgi->end_html();
