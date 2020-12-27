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

use CGI;
use CGI::Session;
use DBI;
use Time::Format qw(time_format %time %strftime %manip);
$cgi  = new CGI;
use CGI qw(:standard escapeHTML);
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$user = "Josh Dunne XXXX"; #$ENV{"REMOTE_USER"};
$user =~ s/IOINTEGRATION\\//g;
$dbh = getDBConnection();	
$dbh-> {'LongReadLen'} = 1000000; 
print $cgi->header();
my $session  = CGI::Session->new($cgi) or die CGI->Session->errstr;
$user = $session->param('sub_e_mail');
print $cgi->start_html(-title=>"Tickets");
print "<script language='javascript'>
function changeText(thisField,thisText)
{
	//alert(thisField + ',' + thisText);
	//setTimeout(thisField.value = thisText,'1000000');
	
}
function confirmDelete(caseNum)
{
	if (confirm(\"Are you sure you want to delete ticket # \" + caseNum))
	{
		location.replace('/cgi-bin/deleteTickets.cgi?selrow=' + caseNum);
	}
}
function confirmClose(caseNum, closeType)
{
        if(confirm('Are you sure you want to close ticket # ' + caseNum))
        {
                window.location = 'helpdesk.cgi?closeTicket=' + closeType + '&case_num=' + caseNum;
        }
}
function selectAction(action, caseNum)
{
	switch(action)
	{
		case \"change\":
			window.location = \"changeContact.cgi?selrow=\" + caseNum;
			break;
		case \"append\":
			window.location = \"appendTicket.cgi?selrow=\" + caseNum;
			break;
		case \"close\":
			confirmClose(caseNum, 'yes');
			break;
		case \"closeNoResp\":
			confirmClose(caseNum, 'noResponse');
			break;
		case \"delete\":
			confirmDelete(caseNum);
			break;
		default:
			break;
	}
}
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
$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '%theapsgroup.com' AND status <> 'Closed' AND status <> 'Awaiting Bug Fix' AND status <> 'Awaiting Feature Request' ORDER BY " . $order_by;
$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '%theapsgroup.com' ORDER BY " . $order_by;
$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '%theapsgroup.com' AND status = 'Awaiting Bug Fix' ORDER BY " . $order_by if (param('showBugTickets'));
$statement = "SELECT status, submitted_by, case_num, date_mod, time_mod, short_desc, prob_prod_link, prob_comp_link, updated_by, priority_type, assigned_to FROM problems WHERE submitted_by like '%theapsgroup.com' AND status = 'Awaiting Feature Request' ORDER BY " . $order_by if (param('showFeatureTickets'));
$showTicketsEnding = "&showBugTickets=yes" if (param('showBugTickets'));
$showTicketsEnding = "&showFeatureTickets=yes" if (param('showFeatureTickets'));
$test = $dbh->prepare($statement);
$test->execute(); 
my $modified = $cgi->param('modified');
ioiFont("<b>Your ticket has been successfully updated</b>") if ($submit eq "yes");
ioiFont("<p><a href = 'hd-respondTicket.cgi?case_num=$modified&user=$user'>Click Here to Modify Your Recently Updated Ticket</a></p>") if ($modified);
print "<div style=\"float: right;\">";
ioiFont ("<input id='submit-ticket' type='button' value='Submit Ticket' onclick=\"window.location='hd-submit-ticket.cgi'\"/>&nbsp;&nbsp;");
print "<input id='logout' type='button' value='Logout' onclick=\"window.location='hd-logout.cgi'\"/>";
print "</div>";
print "<div align ='center'>Active Tickets for $user</div><p>";
#print "<table border='1' cellpadding ='1' cellspacing='1' width ='90%' bgcolor='#909090' align='center'>
ioiFont("<a href='helpdesk.cgi'>Back to my Active Tickets</a><p>") if (param('showFeatureTickets') or param('showBugTickets'));

 tableHead('90%');
 print"
 <th><a href='helpdesk.cgi?order_by=case_num$showTicketsEnding'>Case Number</a></th><th><a href='helpdesk.cgi?order_by=submitted_by$showTicketsEnding'>Submitted By</a></th><th><a href='helpdesk.cgi?order_by=short_desc$showTicketsEnding'>Subject</a></th><th><a href='helpdesk.cgi?order_by=date_mod$showTicketsEnding'>Last Modified</a></th><th><a href='helpdesk.cgi?order_by=status$showTicketsEnding'>Status</a></th><th>Assigned To</th>";
 while(($status, $submitted_by, $case_num, $date_mod, $time_mod, $short_desc, $prob_prod_link, $prob_comp_link, $updated_by , $priority, $assigned_to) = $test->fetchrow_array())
 {

	$bgcolor = '#B0B0B0';
	$short_desc = "<b><font color='blue'>" . $short_desc . "</font></b>" if (lc($updated_by) ne lc($user));
	
	$date_mod =~ s/00:00:00//g;
	$statement = "SELECT sub_name FROM users WHERE sub_login = '$submitted_by'";
	$customer = $dbh->prepare($statement);
	$customer->execute();
	$sub_name = $customer->fetchrow_array();
	$compName = selectValues("SELECT comp_name FROM company WHERE comp_case_num = '$prob_comp_link'");
	$statement = "SELECT contract_type FROM contract WHERE contract_comp_link = (SELECT sub_comp_link FROM users WHERE sub_login='$submitted_by')";
	$contract = selectValues($statement);
	$bgcolor2 = "";
	$bgcolor3 = "";
	$bgcolor2 = "#CCCCCC" if ($contract eq "Platinum");
	$bgcolor2 = "#999933" if ($contract eq "Gold");
	$bgcolor2 = "#999999" if ($contract eq "Silver");
	#$bgcolor2 = "#996600" if ($contract eq "Bronze");
	$bgcolor3 = "red" if ($priority eq "Critical");
	$bgcolor3 = "909090" if ($priority eq "High");
	$bgcolor3 = "green" if ($priority eq "Medium");
	$bgcolor3 = "#0066CC" if ($priority eq "Low");
	print "<tr bgcolor='$bgcolor'>
		<td bgcolor = '$bgcolor2'>
			<form action='hd-respondTicket.cgi' name='form1' method='post'>
				<input type='hidden' name='case_num' value='$case_num'>
				<input type='hidden' name='user' value='$user'>
				<input type='submit' value='$case_num' name='Edit' >
			</form>
		</td>
		<td>$sub_name<br /><span style='font-size:small'>$compName</span></td>
		<td>$short_desc</td>
		<td>$date_mod $time_mod</td>
		<td bgcolor='$bgcolor3'>$status</td>
		<td> $assigned_to</td></tr>";	
 }
 print "</table>";
 ioiFont("The blue subject lines represent tickets that were last updated by someone other than $user");
 ioiFont("<a href='helpdesk.cgi?showBugTickets=yes'>View tickets awaiting bug fix</a><p>");
 ioiFont("<a href='helpdesk.cgi?showFeatureTickets=yes'>View tickets awaiting feature requests");
 print $cgi->end_html;	
