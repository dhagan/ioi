#!/usr/bin/perl

################################################################################
#
#       File Name: appendTicket.cgi
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

print "<h3><center>Append to ticket</h3>";
$case_num = $cgi->param('selrow');
my $dbh = getDBConnection();

$sth = $dbh->prepare("SELECT short_desc,submitted_by FROM problems WHERE case_num = '$case_num'");
$sth->execute();
($short_desc,$submitted_by) = $sth->fetchrow_array();
$new_short_desc = "%$short_desc%";
$sth = $dbh->prepare("SELECT case_num,short_desc,submitted_by,id_num,time_mod,date_mod,status FROM problem WHERE (short_desc like ? or submitted_by='$submitted_by') and (case_num <> '$case_num' and status <> 'Closed')");
$sth->execute($new_short_desc);
print "<center>Suggestions for <b>$short_desc ($case_num)</b></center><p>";
print "<table border='1' align='center' cellspacing='0' width='95%' cellpadding='5' bordercolor='#C0C0C0' bgcolor='#909090'>
<th span= 'row'>Case Number</th><th>Short Description</th><th>Submitted By</th><th>Status</th><th>Last Modified</th><th>Append</th>";
$resultCheck = 0;
while(($case_nums,$short_descs,$submitted_bys,$id_nums,$time_mod,$date_mod,$status) = $sth->fetchrow_array())
{
	print "<form action='appendTicketRes.cgi' method='get'><tr><td><input type ='hidden' name ='from' value='$case_num'><input type='hidden' name='to' value='$case_nums'>
	<a href = 'respondTicket.cgi?viewTicket=yes&case_num=$case_nums'>$case_nums</a></td><td>$short_descs</td><td>$submitted_bys</td><td>$status</td><td>$time_mod $date_mod</td><td><input type = 'submit' name='Append' value='Append'></form>";
	$resultCheck++;
}

$sth = $dbh->prepare("SELECT sub_name,sub_login FROM users ORDER BY sub_name");
$sth->execute();

print "</table>";
if ($resultCheck == 0)
{
print "<font color = '#C0C0C0'><center>No Suggestions for this ticket</center></font>";1
}
print"
<p>
<form action = 'appendSearch.cgi' method = 'get'><center>
Search for ticket to append to: <p>
<table border='1' align='center' cellspacing='0' width='95%' cellpadding='5' bordercolor='#C0C0C0' bgcolor='#909090'>
<tr><td>Ticket #: </td><td><input type='text' name='ticket_num'></td></tr><tr><td>
Customer</td><td><select name='customer'><option value=''> </option>";
while(($sub_names,$sub_logins) = $sth->fetchrow_array)
{
	print "<option value='$sub_logins'>$sub_names</option>";
}
print "
</select></td></tr><tr><td>Assigned To</td><td><select name='assigned_to'><option value=''></option>";
$sth = $dbh->prepare("SELECT sa_name,sa_login FROM staff ORDER BY sa_name");
$sth->execute();
while(($sa_name,$sa_login) = $sth->fetchrow_array())
{
	print "<option value = '$sa_login'>$sa_name</option>";
}
print"</select></td></tr>
<tr><td>Status</td><td><select name = 'status'><option value =''></option>
<option value ='Assigned'>Assigned</option>
<option value ='In Progress'>In Progress</option>
<option value='Pending IOI'>Pending IOI</option>
<option value='Follow Up'>Follow Up</option>
<option value='Pending Client'>Pending Client</option>
<option value='Pending Vendor'>Pending Vendor</option>
<option value='Awaiting Bug Fix>Awaiting Bug Fix</option>
<option value='Awaiting Feature Request'>Awaiting Feature Request</option>
<option value='Closed'>Closed</option>
<option value='Open'>Open</option>
</select></td></tr>
</table>
<input type='submit' name='search' value='Search'>
<input type='hidden' name='case_num' value='$case_num'>
</form></center>";


print $cgi->end_html;