#!/usr/bin/perl

################################################################################
#
#       File Name: staffAppendRes.cgi
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
#       03/29/2007      B. Scarborough  Modified to add generic sendMail function
################################################################################

$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
#staffAppendRes.cgi	
use CGI;
use DBI;
$cgi = new CGI;
$case_num = $cgi->param('case_num');
$newProblem = $cgi->param('problem');
$inputBy = $cgi->param('inputBy');
$customer = $cgi->param('customer');
$company = $cgi->param('company');
$phone = $cgi->param('phone');
my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 1000000; 
$sth = $dbh->prepare("select problem,status,assigned_to from problem where case_num = '$case_num'");
$sth->execute();
($problem,$status,$assigned_to) = $sth->fetchrow_array();
$time=localtime;
$dbproblem = $problem . "\n" . $newProblem . "\n[-Pending IOI- $time $date - $inputBy - Ticket Updated by $inputBy -] \n";
$dbproblem = $dbh->quote($dbproblem);
$statement = "update problem set problem = $dbproblem, status = 'Pending IOI' where case_num = '$case_num'";
$sth = $dbh->prepare($statement);
$sth->execute();
$dbh->commit();

print $cgi->header();
print $cgi->start_html();
print"
<style type=\"text/css\">
<!--
body {
	background-color: #C0C0C0;
}

-->
</style>";
my $awayStatus = 0;
$awayStatus = 1 if (checkTechStatus($assigned_to) eq "away");

$statement = "select sa_login,sa_e_mail from staff where sa_login = '$assigned_to'" if ($assigned_to ne "nobody");
$statement = "select sa_login,sa_e_mail from staff where sa_dept ='IT' and sa_access <> 'Disabled'" if ($assigned_to eq "nobody" or $awayStatus == 1);

$sth = $dbh->prepare($statement);
$sth->execute();
while (($sa_login,$sa_email)= $sth->fetchrow_array())
{
	$email_body = "This ticket $case_num has been updated for $customer at $company. 

Phone: $phone

Problem: $newProblem

This Ticket is currently assigned to $assigned_to.

To update this ticket go to http://dashboard.iointegration.com/cgi-bin/respondTicket.cgi?case_num=$case_num&user=$sa_login&staffmember=$inputBy.

This message was taken by $inputBy";
	$email_body = "This ticket is assigned to $assigned_to, who is currently unavailable right now. Please determine if this ticket requires attention.\n\n" . $email_body if ($awayStatus == 1);
        sendMail($sa_email, "Ticket $case_num has been updated by $inputBy", $email_body);
}		
$dbh->disconnect();

print "<style type='text/css'>
<!--
body {
	background-color: #C0C0C0;
	
}
.style1 {color: #FF9900}
-->
</style>";



print "<div align='center' class='style1'>Ticket $case_num has been updated, an email has been send to IOI Support<p>
Click <a href='customerLookup.cgi'>here</a> to return to the search page</div>";
print $cgi->end_html();