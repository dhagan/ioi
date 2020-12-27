#!/usr/bin/perl

################################################################################
#
#       File Name: helpdesk.cgi
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
#       02/09/2007      B. Scarborough  Modified to allow for recently modified ticket link
#       07/09/2007      B. Scarborough  Modified to display company name on Active Tickets page
################################################################################

use CGI qw(:standard escapeHTML);
use CGI::Session;
use DBI;
use Time::Format qw(time_format %time %strftime %manip);
$cgi  = new CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";

($sub_e_mail, $sub_name, $sub_comp_link) = &getUserSession();
if (!$sub_e_mail || !$sub_name || !$sub_comp_link) {
   print $cgi->header();
   print "You appear to be logged out, please login";
   print "<input id='login' type='button' value='Login' onclick=\"window.location='hd-login.cgi'\"/>";
   exit;
}


$user=$sub_e_mail;
$dbh = getDBConnection();	
$dbh-> {'LongReadLen'} = 1000000; 
print $cgi->header();
print $cgi->start_html(-title=>"Tickets");
print "
</script>
<style type='text/css'>
<!--
.linkLook {
	color: #0033CC;
	text-decoration: underline;
}
.linkLook:hover
{	
cursor:pointer;
}
-->
</style>";
if (param('closeTicket') eq "yes")
{
	$case_num = param('case_num');
	insert("UPDATE problems SET status = 'Closed' WHERE case_num='$case_num'");
}
if (param('closeTicket') eq "noResponse")
{
	my $date=time_format('yyyy/mm/dd');
	my $time = $time{"hh:mm:ss"};	
	$case_num = param('case_num');
	insert("UPDATE problems SET status = 'Closed' WHERE case_num = '$case_num'");
        $sth = $dbh->prepare("SELECT id FROM problems WHERE case_num = '$case_num'");
        $sth->execute();
        my $problem_id = $sth->fetchrow_array();
        my $description = quoteValues($problem);
        my $description_updated_by = $dbh->quote("$user");
        my $action = "Updated by $user";
        my $is_customer = false;
        my $statement = "INSERT INTO `descriptions` (problem_id, description, status, created, description_updated_by, action, is_customer) VALUES ('$problem_id', $description, 'Closed (no response)', NOW(), $description_updated_by, '$action', '$is_customer')";
	
}

$submit = $cgi->param('submit');
$order_by = $cgi->param('order_by');
$order_by = 'case_num' if ($order_by eq "");
autoRefresh();
background();
$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '$user' AND status <> 'Closed' AND status <> 'Awaiting Bug Fix' AND status <> 'Awaiting Feature Request' AND status <> 'Deleted' ORDER BY " . $order_by;
#$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '$user' ORDER BY " . $order_by;
$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '$user' AND status = 'Awaiting Bug Fix' ORDER BY " . $order_by if (param('showBugTickets'));
$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '$user' AND status = 'Awaiting Feature Request' ORDER BY " . $order_by if (param('showFeatureTickets'));
$showTicketsEnding = "&showBugTickets=yes" if (param('showBugTickets'));
$showTicketsEnding = "&showFeatureTickets=yes" if (param('showFeatureTickets'));
$test = $dbh->prepare($statement);
$test->execute(); 
my $modified = $cgi->param('modified');
ioiFont("<b>Your ticket has been successfully updated</b>") if ($submit eq "yes");
print "<div style=\"float: right;\">";
ioiFont ("<input id='submit-ticket' type='button' value='Create Ticket' onclick=\"window.location='hd-submitTicket.cgi'\"/>&nbsp;&nbsp;");
print "<input id='logout' type='button' value='Logout' onclick=\"window.location='hd-logout.cgi'\"/>";
print "</div>";
print "<div align ='center'>Active Tickets for $sub_name</div><p>";
#print "<table border='1' cellpadding ='1' cellspacing='1' width ='90%' bgcolor='#909090' align='center'>
ioiFont("<a href='helpdesk.cgi'>Back to my Active Tickets</a><p>") if (param('showFeatureTickets') or param('showBugTickets'));

 tableHead('100%');
 print"
 <th><a href='helpdesk.cgi?order_by=case_num$showTicketsEnding'>Case Number</a></th></th><th><a href='helpdesk.cgi?order_by=short_desc$showTicketsEnding'>Subject</a></th><th><a href='helpdesk.cgi?order_by=date_mod$showTicketsEnding'>Last Modified</a></th><th><a href='helpdesk.cgi?order_by=status$showTicketsEnding'>Status</a></th><th>Assigned To</th>";
 @bgcolors=("#ffffff","f8f8f8");
 $row=0;
 while(($status, $submitted_by, $case_num, $date_mod, $time_mod, $short_desc, $prob_prod_link, $prob_comp_link, $updated_by , $priority, $assigned_to) = $test->fetchrow_array())
 {

	$short_desc = "<b>" . $short_desc . "</font></b>" if (lc($updated_by) ne lc($user));
	$date_mod =~ s/00:00:00//g;
	$statement = "SELECT sub_name FROM users WHERE sub_login = '$submitted_by'";
	$customer = $dbh->prepare($statement);
	$customer->execute();
	$sub_name = $customer->fetchrow_array();
	$compName = selectValues("SELECT comp_name FROM company WHERE comp_case_num = '$prob_comp_link'");
	$statement = "SELECT contract_type FROM contract WHERE contract_comp_link = (SELECT sub_comp_link FROM users WHERE sub_login='$submitted_by')";
	$contract = selectValues($statement);
	$bgcolor = "";
	$bgcolor2 = "";
	$bgcolor3 = "";
#	$bgcolor2 = "#CCCCCC" if ($contract eq "Platinum");
#	$bgcolor2 = "#999933" if ($contract eq "Gold");
#	$bgcolor2 = "#999999" if ($contract eq "Silver");
#	#$bgcolor2 = "#996600" if ($contract eq "Bronze");
#	$bgcolor3 = "red" if ($priority eq "Critical");
#	$bgcolor3 = "909090" if ($priority eq "High");
#	$bgcolor3 = "green" if ($priority eq "Medium");
#	$bgcolor3 = "#0066CC" if ($priority eq "Low");
	$bgcolor = $bgcolors[$row %2];
	$row++;
	print "<tr bgcolor='$bgcolor'>
		<td bgcolor = '$bgcolor2'>
			<form action='hd-respondTicket.cgi' name='form1' method='post'>
				<input type='hidden' name='case_num' value='$case_num'>
				<input type='hidden' name='user' value='$user'>
				<input type='submit' value='$case_num' name='Edit' >
			</form>
		</td>
		<td>$short_desc</td>
		<td>$date_mod $time_mod</td>
		<td bgcolor='$bgcolor3'>$status</td>
		<td> $assigned_to</td></tr>";	
 }
 print "</table>";
 print $cgi->end_html;	
