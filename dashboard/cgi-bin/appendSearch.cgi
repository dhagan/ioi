#!/usr/bin/perl

################################################################################
#
#       File Name: appendSearch.cgi
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

use CGI;
use DBI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
print $cgi->header();
print $cgi->start_html();
print "<style type='text/css'>
		<!--
		body {
			background-color: #C0C0C0;
		}
		
		-->
		</style>";
$customer = $cgi->param('customer');
$case_num = $cgi->param('ticket_num');
#$case_num = $cgi->param('ticket');
$status = $cgi->param('status');
$assigned_to = $cgi->param('assigned_to');
$from = $cgi->param('case_num');

my $dbh = getDBConnection();
if($customer ne "" and $case_num ne "" and $status ne "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num' 
	and submitted_by = '$customer' and assigned_to = '$assigned_to' and status = '$status'";
}
elsif ( $customer ne "" and $case_num ne "" and $status ne "" and $assigned_to eq "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num' 
	and submitted_by = '$customer' and  status = '$status'";
}
elsif ($customer ne "" and $case_num ne "" and $status eq "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num' 
	and submitted_by = '$customer' and assigned_to = '$assigned_to'";
}
elsif($customer ne "" and $case_num eq "" and $status ne "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where 
	 submitted_by = '$customer' and assigned_to = '$assigned_to' and status = '$status'";
}
elsif($customer eq "" and $case_num ne "" and $status ne "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num' 
	and  assigned_to = '$assigned_to' and status = '$status'";
}
elsif($customer ne "" and $case_num ne "" and $status eq "" and $assigned_to eq "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num' 
	and submitted_by = '$customer'";
}
elsif($customer ne "" and $case_num eq "" and $status ne "" and $assigned_to eq "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where 
	 submitted_by = '$customer'  and status = '$status'";
}
elsif($customer ne "" and $case_num eq "" and $status eq "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where submitted_by = '$customer' and assigned_to = '$assigned_to' ";
}
elsif($customer ne "" and $case_num eq "" and $status eq "" and $assigned_to eq "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where submitted_by = '$customer'";
}
elsif($customer eq "" and $case_num ne "" and $status ne "" and $assigned_to eq "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num' 
	 and status = '$status'";
}
elsif($customer eq "" and $case_num ne "" and $status eq "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num' 
	 and assigned_to = '$assigned_to' ";
}
elsif($customer eq "" and $case_num ne "" and $status eq "" and $assigned_to eq "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where case_num like '%$case_num'";
}
elsif($customer eq "" and $case_num eq "" and $status ne "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where 
	 assigned_to = '$assigned_to' and status = '$status'";
}
elsif($customer eq "" and $case_num eq "" and $status ne "" and $assigned_to eq "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where  status = '$status'";
}
elsif($customer eq "" and $case_num eq "" and $status eq "" and $assigned_to ne "")
{
	$statement = "Select case_num,short_desc,submitted_by,time_mod from problem where assigned_to = '$assigned_to' ";
}
else {print "Please Enter Search Criteria";}

$sth = $dbh->prepare($statement);
$sth->execute();
print "<table border='1' align='center' cellspacing='0' width='95%' cellpadding='5' bgcolor='#909090' bordercolor='#C0C0C0'>
<th>#</th><th span= 'row'>Case Number</th><th>Short Description</th><th>Submitted By</th><th>Last Modified</th><th>Append</th>";
$i=1;
while(($case_nums,$short_descs,$submitted_bys,$time_mod) = $sth->fetchrow_array())
{
	print "<form action='appendTicketRes.cgi' method='get'><tr><td>$i<td><input type ='hidden' name ='from' value='$from'><input type='hidden' name='to' value='$case_nums'>
	<a href = 'viewPage.cgi?case_num=$case_nums'>$case_nums</a></td><td>$short_descs</td><td>$submitted_bys</td><td>$time_mod</td><td><input type = 'submit' name='Append' value='Append'></form>";
	$i++;
}
print "</table>";