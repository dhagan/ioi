#!/usr/bin/perl

################################################################################
#
#       File Name: dailyactivity.cgi
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
#       02/27/2007      B. Scarborough  Modified newRequest and createReport to update staffDropDown function call
#       03/29/2007      B. Scarborough  Modified to use generic sendMail and sendMailWithAttachment functions
#       06/04/2007      B. Scarborough  Modified to support new sendMailWithAttachment to go with new SubmitMail.cgi
################################################################################

use Time::Format qw(time_format %time);
use CGI;
use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
$date=time_format('m-dd-yyyy');
$time{$format};
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
$days = param('daily_activity');
$days = 0 if !($days);
### DJH $user = $ENV{REMOTE_USER};
$user = getRemoteUser();
my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 2000000;

if (param('show_tickets_status'))
	{
		showStatusTickets();
	}
elsif (param('show_tickets_login'))
{
	showLoginTickets();
}
elsif (param('createReport'))
{
	createReport();
}
elsif (param('createReportRes'))
{
	createReportRes();
}
elsif (param('featureRequest'))
{
	featureRequest() if (param('featureRequest') eq "view");
	updateRequest() if (param('featureRequest') eq "update");
	newRequest() if (param('featureRequest') eq "new");
	newRequestRes() if (param('featureRequest') eq "newRes");
	updateRequestRes() if (param('featureRequest') eq "updateRes");
	developer() if (param('featureRequest') eq "developer");
	developerRes() if (param('featureRequest') eq "developerRes");
}
else
{
	showDailyActivity();
}





sub showDailyActivity()
{
	print $cgi->header();
	headers();
	menu_focus();
	background();
	bodyAndLoad("menu_focus(document.form1.daily_activity,\"$days\")");
	ioiFont("Daily Activity for");
	print "<form name='form1' action ='' id='form1' >
			<div align='center'><select name= 'daily_activity' onChange='document.form1.submit()'>
			<option value='0'>Today ($date)</option>
			<option value='7'>Last 7 Days</option>
			<option value='14'>Last 14 days</option>
			<option value='30'>Last 30 days</option></select></div></form>";
	tableHead('25%');
	print "<tr><div align='center'>"; ioiFont("Ticket Breakdown");
	print "</div></tr>";
	$login = $dbh->prepare("select sa_login,sa_name from staff where (sa_dept = 'IT' and sa_access = 'Active') or sa_login ='nobody'");
	$login->execute();
	while (($sa_login,$sa_name) = $login->fetchrow_array())
	{
		print "<tr><td><a href='dailyActivity.cgi?show_tickets_login=$sa_login&days=$days'>$sa_name</a></td>\n";
		$statement ="select count(case_num) from problem where CURDATE() = date_mod and assigned_to = '$sa_login'" if ($days == 0);
		$todays_count = "select count(case_num) from problem where CURDATE() = date_mod and CURDATE() = date_open and assigned_to ='$sa_login'";
		$statement ="select count(case_num) from problem where DATE_SUB(CURDATE(),INTERVAL 7 DAY) <= date_mod and assigned_to = '$sa_login'" if ($days == 7);
		$statement ="select count(case_num) from problem where DATE_SUB(CURDATE(), INTERVAL 14 DAY) <= date_mod and assigned_to = '$sa_login'" if ($days == 14);
		$statement ="select count(case_num) from problem where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date_mod and assigned_to = '$sa_login'" if ($days == 30);
		
		$sth = $dbh->prepare($statement);	
		$sth->execute();
		$count = $sth->fetchrow_array();
		$todays_count = $dbh->prepare($todays_count);
		$todays_count->execute();
		$todays_count = $todays_count->fetchrow_array();
		print "<td>$count&nbsp;";
		print "($todays_count)" if ($days == 0);
		print"</td></tr>\n";
	}
	print "</table>";
	
	ioiFont("Ticket States");
	tableHead('25%');
	$status = $dbh->prepare("select field_data from dynamic_fields where field_name = 'status'");
	$status->execute();
	$status = $status->fetchrow_array();
	$status =~ s/\n//;
	@status = split(/;/,$status);
	foreach $thisStatus(@status)
	{
		$thisStatus =~ s/^\s*//;
		print "<tr><td><a href='dailyActivity.cgi?show_tickets_status=$thisStatus&days=$days'>$thisStatus</td>";
		$statement = "select count(case_num) from problem where CURDATE() = date_mod and status = '$thisStatus'" if ($days == 0);
		$statement = "select count(case_num) from problem where DATE_SUB(CURDATE(),INTERVAL 7 DAY) <= date_mod and status = '$thisStatus'" if ($days == 7);
		$statement = "select count(case_num) from problem where DATE_SUB(CURDATE(), INTERVAL 14 DAY) <= date_mod and status = '$thisStatus'" if ($days == 14);
		$statement = "select count(case_num) from problem where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date_mod and status = '$thisStatus'" if ($days == 30);
		$sth = $dbh->prepare($statement);
		$sth->execute();
		$count= $sth->fetchrow_array();
		# while(@row = $sth->fetchrow_array())
	# 	{
	# 	$count++;
	# 	}
		print "<td>$count</td></tr>\n";
	}
}




sub showStatusTickets()
{
	print $cgi->header();
	headers();
	menu_focus();
	background();
	bodyAndLoad("menu_focus(document.form1.daily_activity,\"$days\")");
	$days = param('days');
	$order_by = param('order_by');
	$order_by = "case_num" if !($order_by);
	$date = "CURDATE() " if ($days == 0);
	$date = "DATE_SUB(CURDATE(),INTERVAL 7 DAY) " if ($days == 7);
	$date = "DATE_SUB(CURDATE(),INTERVAL 14 DAY) " if ($days == 14);
	$date = "DATE_SUB(CURDATE(),INTERVAL 30 DAY) " if ($days == 30);
	$status = param('show_tickets_status');
	### DJH $user = $ENV{"REMOTE_USER"};
	### DJH $user =~ s/IOINTEGRATION\\//g;
	$user = getRemoteUser();
	tableHead('90%');
	print "<tr><td>Select</td><td><a href='dailyActivity.cgi?order_by=case_num&show_tickets_status=$status&days=$days'>Ticket #</a></td>
	<td><a href='dailyActivity.cgi?order_by=short_desc&show_tickets_status=$status&days=$days'>Subject</a></td>
	<td>Assigned To</td><td><a href='dailyActivity.cgi?order_by=submitted_by&show_tickets_status=$status&days=$days'>Submitted By</a></td>
	<td><a href='dailyActivity.cgi?order_by=status&show_tickets_status=$status&days=$days'>Status</a></td><td><a href='dailyActivity.cgi?order_by=xinet_ticket_num&show_tickets_status=$status&days=$days'>Vendor Ticket #</td>
	<td><a href='dailyActivity.cgi?order_by=date_mod&show_tickets_status=$status&days=$days'>Last Modified</a></td><td>Change Contact</td><td>Update</td></tr>";
	searchTickets("status ='$status' and $date <= date_mod",$user,$order_by);
	print "<div align='center'><a href='dailyActivity.cgi?daily_activity=$days'>Go back to Daily Activity</a></div>";
}
sub showLoginTickets()
{
	print $cgi->header();
	headers();
	menu_focus();
	background();
	bodyAndLoad("menu_focus(document.form1.daily_activity,\"$days\")");
	$order_by = param('order_by');
	$order_by = "case_num" if !($order_by);
	$days = param('days');
	$date = "CURDATE() " if ($days == 0);
	$date = "DATE_SUB(CURDATE(),INTERVAL 7 DAY) " if ($days == 7);
	$date = "DATE_SUB(CURDATE(),INTERVAL 14 DAY) " if ($days == 14);
	$date = "DATE_SUB(CURDATE(),INTERVAL 30 DAY) " if ($days == 30);
	$sa_login = param('show_tickets_login');
	###$user = $ENV{"REMOTE_USER"};
	###$user =~ s/IOINTEGRATION\\//g;
        $user = getRemoteUser();
	tableHead('90%');
	print "<tr><td>Select</td><td><a href='dailyActivity.cgi?order_by=case_num&show_tickets_login=$sa_login&days=$days'>Ticket #</a></td>
	<td><a href='dailyActivity.cgi?order_by=short_desc&show_tickets_login=$sa_login&days=$days'>Subject</a></td>
	<td>Assigned To</td><td><a href='dailyActivity.cgi?order_by=submitted_by&show_tickets_login=$sa_login&days=$days'>Submitted By</a></td>
	<td><a href='dailyActivity.cgi?order_by=status&show_tickets_login=$sa_login&days=$days'>Status</a></td><td><a href='dailyActivity.cgi?order_by=xinet_ticket_num&show_tickets_login=$sa_login&days=$days'>Vendor Ticket #</td>
	<td><a href='dailyActivity.cgi?order_by=date_mod&show_tickets_login=$sa_login&days=$days'>Last Modified</a></td><td>Change Contact</td><td>Update</td></tr>";
	searchTickets("assigned_to ='$sa_login' and $date <= date_mod ",$user,$order_by);
	print "<div align='center'><a href='dailyActivity.cgi?daily_activity=$days'>Go back to Daily Activity</a></div>";
}
sub createReport()
{
	print $cgi->header();
	headers();
	background();
	print "<script language='javascript'>
	function quickReports(thisReport)
	{
		document.quickReport.action.value = thisReport;
		if (document.quickReport.assigned_to.value == '')
		{
			alert('Please select a staff member to send this to.');
		}
		else {
		
		document.quickReport.submit();
		return true;
		}
	}
	</script>";
	bodyAndLoad();
	
	ioiFont("Quick Reports");
	tableHead('65%');
	print "<tr><form name='quickReport' id='quickReport' method='get'>
	<input type='hidden' name='action' value=''>
	<input type='hidden' name='createReportRes' value='yes'>
	<td colspan='1'>Send to</td><td>";
	staffDropDown("assigned_to", "true");
	print "</td></tr>";
	print "\n<tr><td>Customer Email,First Name,Last Name</td><td><input type='button' name='Report' value='Generate' onClick='quickReports(\"customer_emails\")'></td></tr>
			 <tr><td>Support Expiring < 30 days</td><td><input type='button' name='Report' value='Generate' onClick='quickReports(\"expired_contracts\")'></td></tr>
			 <tr><td>Company 12 month ticket report</td><td>(You may select multiple companies)";
			 companyDropDown("5");
			 print"<input type='button' name='Report' value='Generate' onClick='quickReports(\"company_tickets\")'></td></tr>
	
	
	</table></form>";
}
sub createReportRes()
{
	$action = param('action');
	$staff = param('assigned_to');
	@companies = param('company');
	$email = selectValues("select sa_e_mail from staff where sa_login = '$staff'");
	createCustomerEmailReport($email) if ($action eq "customer_emails");
	expiredContracts($email) if ($action eq "expired_contracts");
	companyTickets($email) if ($action eq "company_tickets");
}
sub companyTickets()
{
	@companies=param('company');
	$email = $_[0];
	use DBI;
	open (FILE,">/Library/WebServer/dashboard/reports/report-$date.csv");
	print FILE "Company,Total Tickets,Closed Tickets,Pending IOI,Awaiting Bug/Feature Request\n";
	eval{
	foreach $company(@companies)
	{
		$login = $dbh->prepare("select sub_login from users where sub_comp_link = '$company'");
		$login->execute();
		while ($sub_login = $login->fetchrow_array())
		{
			$c_count=$dbh->prepare("select count(case_num) from problem where status = 'Closed' and submitted_by='$sub_login' and date_mod > DATE_SUB(CURDATE(),INTERVAL 365 DAY)");
			$t_count =$dbh->prepare("select count(case_num) from problem where submitted_by ='$sub_login' and date_mod >DATE_SUB(CURDATE(),INTERVAL 365 DAY)");
			$i_count = $dbh->prepare("select count(case_num) from problem where submitted_by = '$sub_login' and status= 'Pending IOI' and date_mod > DATE_SUB(CURDATE(),INTERVAL 365 DAY)");
			$a_count = $dbh->prepare("select count(case_num) from problem where submitted_by = '$sub_login' and (status = 'Awaiting Bug Fix' or status = 'Awaiting Feature Request') and date_mod > DATE_SUB(CURDATE(),INTERVAL 365 DAY)");
			$c_count->execute();
			$t_count->execute();
			$i_count->execute();
			$a_count->execute();
			$closed_count += $c_count->fetchrow_array();
			$total_count += $t_count->fetchrow_array();
			$ioi_count += $i_count->fetchrow_array();
			$awaiting_count += $a_count->fetchrow_array();
			
		
		}
		($comp_name) = selectValues("select comp_name from company where comp_case_num = '$company'");
		print FILE "$comp_name,$total_count,$closed_count,$ioi_count,$awaiting_count\n";
		$closed_count = 0;
		$total_count= 0;
		$ioi_count = 0;
		$awaiting_count = 0;
	}
	};
	close FILE;
	print "Failed" if ($@);
	emailReport("report-$date.csv",$email);
}
	
sub createCustomerEmailReport()
{
	$email = $_[0];
	use DBI;
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000; 

	$sth = $dbh->prepare("select sub_e_mail,sub_name from users");
	$sth->execute();
	$i = 0;
open (FILE,">/Library/WebServer/dashboard/reports/report-$date.csv") or die "could not open file";

	while(($sub_e_mail,$sub_name) = $sth->fetchrow_array())
	{
		if ($sub_e_mail =~ /iointegration.com/ || $sub_e_mail =~ /innovate/)
		{
		}
		else
		{
		@name = split(/ /,$sub_name);
		print FILE ("\"$sub_e_mail\",\"@name[0]\",\"@name[1]\",\n");
		@emails[$i] = $sub_e_mail;
		@names[$i] = $sub_name;
		}
	}

close FILE;
emailReport("report-$date.csv",$email);
}
sub expiredContracts()
{
	
	$email = $_[0];
	use DBI;
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 1000000; 
	open (FILE,">/Library/WebServer/dashboard/reports/expired_contracts-$date.csv");
	print FILE "Company Name,Company Phone,Contract Type,Contract Exp Date";
	$contract = $dbh->prepare("select contract_comp_link,contract_type,contract_date_expired from contract where contract_date_expired <= DATE_SUB(CURDATE(),INTERVAL 30 DAY)");
	$contract->execute();
	while(($contract_comp_link,$contract_type,$contract_date_expired) = $contract->fetchrow_array())
	{
		($comp_name,$comp_phone) = selectValues("select comp_name,comp_phone from company where comp_case_num = '$contract_comp_link'");
		print FILE "\"$comp_name\",\"$comp_phone\",\"$contract_type\",\"$contract_date_expired\"\n";
	}
	close FILE;
	emailReport("expired_contracts-$date.csv",$email);
}
	

	

sub emailReport()
{
	$filename= $_[0];
	$email = $_[1];
	$upload_directory = "/Library/WebServer/dashboard/reports";
	print $cgi->header();
	headers();
        sendMailWithAttachment($email, "Here is the report you requested", "", "dashboard\@iointegration.com", "", "", "$upload_directory/$filename");
	background();
	bodyAndLoad();
	ioiFont("Your report '$filename' has been sent to $email");
	end_HTML;
}

sub featureRequest()
{
	print $cgi->header();
	headers();
		print "<script>
		function toggle(hidethis) {
 		if( document.getElementById(hidethis).style.display=='none' ){
 		  document.getElementById(hidethis).style.display = '';
 			}else{
  			 document.getElementById(hidethis).style.display = 'none';
 		}
	}
		
</script>
<style type='text/css'>
<!--
.toggle {
	font-family: 'Times New Roman', Times, serif;
	font-size: 16px;
	font-style: oblique;
	line-height: normal;
	color: black;
}
.toggle:hover
{
	text-decoration:underline;
	cursor:pointer;
	text-shadow:Aqua;
}
--></style>";
	background();
	bodyAndLoad('closeTR();');
	tableHead('95%');
	$sth = $dbh->prepare("select request_id,request_name,request_date,request_priority,request_status,request_data,request_subject from feature_request order by request_priority");
	$sth->execute();
	print "<tr><td>Priority #</td><td>Status</td><td>Subject</td><td>Date Submitted</td><td>Submitted By</td><td>Edit/View Details</td>";
	$i= 0;
	while(($request_id,$request_name,$request_date,$request_priority,$request_status,$request_data,$request_subject) = $sth->fetchrow_array())
	{
		$color = 'white' if ($request_status eq "Pending Review");
		$color = '#B0B0B0' if ($request_status eq "In Queue");
		$color = '#FF3300' if ($request_status eq "Critical:Being addressed");
		$color = 'green' if ($request_status eq "Finished");
		$color = 'yellow' if ($request_status eq "Currently being addressed");
		$color = 'gray' if ($request_status eq "Long Term");
		$request_priority = "" if ($request_priority eq "999");
		print "<tr bgcolor='$color'><form name='form1' action ='' method='get'>
		<input type='hidden' name='request_id' value='$request_id'>
		<input type='hidden' name='featureRequest' value='update'>
		<td>$request_priority</td><td>$request_status</td>
		<td>$request_subject</td><td>$request_date</td><td>$request_name</td><td>
		<input type='submit' name='submit' value='Edit'><span class='toggle' onClick=\"toggle('hidethis$i');\">View</span></td></tr></form>
		<tr bgcolor='#B0B0B0' id='hidethis$i'><td colspan='6'><div align='center'><textarea name='request_data' rows='8' cols='75' readonly>$request_data</textarea></div></td></tr></form>";
		$i++;
	}
	print "</table>";
	print "<script language='javascript'>
		function closeTR()
		{
			for(var i = 0; i< $i; i++)
			{
				document.getElementById('hidethis' + i).style.display = 'none';
			}
		}	
		
</script>";
	print"<form name='form2' action ='' method='post'>
	<input type='hidden' name='featureRequest' value='new'>
	<div align='center'><input type='submit' name='submit' value='New Request'></center>
	</form>";
	end_HTML;
	
}
sub newRequest()
{	
	print $cgi->header();
	headers();
	menu_focus();
	print "<script language ='javascript'>
	function checkSubmit()
	{
		if (document.form1.assigned_to.value == '')
		{
			alert('Please select your name');
			return false;
		}
		if (document.form1.request_type.value == '')
		{
			alert('Please select the request type');
			return false;
		}
		if (document.form1.request_subject.value == '')
		{
			alert('You must enter a subject for this request');
			return false;
		}
		return true;
	}
	</script>";
	background();
	bodyAndLoad("menu_focus(document.form1.assigned_to,\"$user\")");
	ioiFont("Create new feature request or bug fix");
	
	tableHead('65%');
	print "<form name='form1' method ='post' action='' onSubmit='return checkSubmit();'>
			<input type='hidden' name='featureRequest' value='newRes'>
			<tr><td>Name:</td><td> ";
	staffDropDown("assigned_to", "true");
	print "</td></tr><tr><td>Request Type: </td><td><select name='request_type'><option =''></option>
	<option value='Bug Fix'>Bug Fix</option><option value='Feature Request'>Feature Request</option></select></td></tr>
		<tr><td>Priority</td><td><select name='priority'><option value='low'>Low</option><option value='Medium'>Medium</option>
		<option value='High'>High</option><option value='critical'>Critical</option></select></td></tr>
		<tr><td>Subject: </td><td><input type='text' name='request_subject' value='' size='50'></td></tr>
		  <tr><td colspan='2'><div align='center'>Detailed Description (If needed)</div></td></tr>
		  <tr><td colspan ='2'><div align='center'><textarea name ='request_data' rows='10' cols='75'></textarea></div></td></tr>
		  <tr><td colspan ='2'><div align='center'><input type='submit' name='submit' value='Submit'></div></td></tr>
		  </table>
		  </form>";
	end_HTML;
}
sub newRequestRes()
{
	my $assigned_to = param('assigned_to');
	my $request_type = param('request_type');
	my $priority = param('priority');
	my $request_subject = param('request_subject');
	my $request_data = param('request_data');
	my $date=time_format('yyyy/mm/dd');
		print $cgi->header();
	$assigned_to = $dbh->quote($assigned_to);
	$request_type = $dbh->quote($request_type);
	$request_subject = $dbh->quote($request_subject);
	$request_data = $dbh->quote($request_data);
	$statement = "Insert into feature_request (request_name,request_priority,request_date,request_status,request_data,request_subject,request_type) values 
				($assigned_to,'999','$date','Pending Review',$request_data,$request_subject,$request_type)";
	insert($statement);
        sendMail("matt\@iointegration.com", "A new $request_type has been submitted by $assigned_to", "Priority: $priority\n\nSubject: $request_subject\n\nDate: $date\n\nProblem: $request_data\n\n http://dashboard.iointegration.com/cgi-bin/dailyActivity.cgi?featureRequest=developer", "featureRequest\@iointegration.com", "nige\@iointegration.com");
	headers();
	background();
	bodyAndLoad();
	ioiFont("Your request has been submitted, your request will be assigned a priority pending review.<p>Click <a href='dailyActivity.cgi?featureRequest=view'>here </a> to go back to the feature request page.");
	end_HTML;
}

	
	
sub updateRequest()
{
	$request_id = param('request_id');
	if ($request_id ne "")
	{
		($request_name,$request_date,$request_priority,$request_status,$request_data,$request_subject) = selectValues("select request_name,request_date,request_priority,request_status,request_data,request_subject from feature_request where request_id='$request_id'");
	}
	print $cgi->header();
	headers();
	print "<script language='javascript'>
	function checkDelete()
	{
		var confirmDelete = confirm('Are you sure you want to delete this request');
		if (confirmDelete)
		{
			document.form1.submit();
		}
		else
		{
			return false;
		}
		return true;
	}
	</script>";
	background();
	bodyAndLoad();
	print "<form name='form1' method='post' action=''>
	<input type='hidden' name='featureRequest' value='updateRes'>
	<input type='hidden' name='request_id' value='$request_id'>";
	tableHead('65%');
	print "<tr><td>Submitted By: <b>$request_name</b></td><td>Date: <b>$request_date</b></td></tr>
		   <tr><td>Priority #: <b>$request_priority</b></td><td>Request Status: <b>$request_status</b></td>
		   <tr><td colspan = '2'><div align='center'>Subjet: <b>$request_subject </b></div></td></tr>
		   <tr><td colspan = '2'><div align='center'>Problem</div></td></tr>
		   <tr><td colspan = '2'><div align='center'><textarea name='request_data' rows = '20' cols='75'>$request_data</textarea></center></td></tr>
		   <tr><td colspan = '2'><div align='center'><input type='submit' name='submit' value='Update'><input type='submit' name='submit' value='Delete Request' onClick='return checkDelete();'></div></td></tr>
		   </table>";
		   end_HTML;
}
sub updateRequestRes()
{
	$request_id = param('request_id');
	$request_data = param('request_data');
	$delete_request = 1 if (param('submit') eq "Delete Request");
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	if ($delete_request ==1)
	{
		$statement = "Delete from feature_request where request_id = '$request_id'";
		$sth = $dbh->prepare($statement);
		$sth->execute();
		$dbh->commit();
		ioiFont("Your request has been deleted. Click <a href='dailyActivity.cgi?featureRequest=view'>here </a> to go back to the feature request page.");
	}
	else
	{
		$request_data = $dbh->quote($request_data);
		$statement = "Update feature_request set request_data = $request_data where request_id = '$request_id'";
		insert($statement);
		ioiFont("Your request has been updated. Click <a href='dailyActivity.cgi?featureRequest=view'>here </a> to go back to the feature request page.");
	}
}
		
sub developer()
{
	print $cgi->header();
	headers();
	print "<script>
function toggle(hidethis) {
 if( document.getElementById(hidethis).style.display=='none' ){
   document.getElementById(hidethis).style.display = '';
 }else{
   document.getElementById(hidethis).style.display = 'none';
 }
}
		
</script>
<style type='text/css'>
<!--
.toggle {
	font-family: 'Times New Roman', Times, serif;
	font-size: 16px;
	font-style: oblique;
	line-height: normal;
	color: black;
}
.toggle:hover
{
	text-decoration:underline;
	cursor:pointer;
	text-shadow:Aqua;
}
--></style>";
	background();
	bodyAndLoad('closeTR()');
	$i = 0;
	tableHead('95%');
		$sth = $dbh->prepare("select request_id,request_name,request_date,request_priority,request_status,request_data,request_subject,request_type from feature_request order by request_priority");
		$sth->execute();
		print "<tr><td>Priority #</td><td>Status</td><td>Subject</td><td>Date Submitted</td><td>Submitted By</td><td>Edit/View Details</td>";
		while(($request_id,$request_name,$request_date,$request_priority,$request_status,$request_data,$request_subject,$request_type) = $sth->fetchrow_array())
		{
		$color = 'white' if ($request_status eq "Pending Review");
		$color = '#B0B0B0' if ($request_status eq "In Queue");
		$color = '#FF3300' if ($request_status eq "Critical:Being addressed");
		$color = 'green' if ($request_status eq "Finished");
		$color = 'yellow' if ($request_status eq "Currently being addressed");
		$color = 'gray' if ($request_status eq "Long Term");
		print "<form name='form1' method='get' action='dailyActivity.cgi'>
				<input type='hidden' name='user' value='$request_name'>
				<input type='hidden' name='request_type' value='$request_type'>
				<input type='hidden' name='request_subject' value='$request_subject'>
				<input type='hidden' name='request_id' value='$request_id'>
				<input type='hidden' name='featureRequest' value='developerRes'>
				<tr bgcolor='$color'><td><input type='text' name='request_priority' value='$request_priority'></td><td><select name='request_status'>
				<option value=''></option>
				<option value='Pending Review'>Pending Review</option>
				<option value='In Queue'>In Queue</option>
				<option value='Currently being addressed'>Currently being addressed</option>
				<option value='Critical:Being addressed'>Critical:Being Addresssed</option>
				<option value='Long Term'>Long Term</option>
				<option value='Finished'>Finished</option>
				</select>Currently: $request_status
				</td><td>$request_subject</td><td>$request_date</td><td>$request_name</td><td><input type='submit' name='update' value='Update'><span class='toggle' onClick=\"toggle('hidethis$i');\">View</span></td></tr>
				<tr bgcolor='#B0B0B0' id='hidethis$i'><td colspan='6'><div align='center'><textarea name='request_data' rows='8' cols='75'>$request_data</textarea></div></td></tr></form>";
				$i++;
		}
		print "</table>";
print "<script language='javascript'>
function closeTR()
{
	for(var i = 0; i< $i; i++)
	{
		document.getElementById('hidethis' + i).style.display = 'none';
	}
}
		
</script>";
		end_HTML;
}
sub developerRes()
{
	$request_id = param('request_id');
	$request_status = param('request_status');
	$request_priority = param('request_priority');
	$request_data = param('request_data');
	$request_type = param('request_type');
	$request_name = param('user');
	$request_subject = param('request_subject');
	($sa_email) = selectValues("select sa_e_mail from staff where sa_login='$request_name'");
        sendMail($sa_email, "Your $request_type has been finished", " Your $request type, '$request_subject', has been completed.\n\nHere is the history:\n\n$request_data", "matt\@iointegration.com", "", "nige\@iointegration.com") if ($request_status eq "Finished");
	$request_data = $dbh->quote($request_data);
	
	if ($request_status ne "")
	{
		$statement = "update feature_request set request_status = '$request_status', request_priority= $request_priority,request_data=$request_data where request_id = $request_id";
	}
	else
	{
		$statement = "update feature_request set request_priority= $request_priority,request_data=$request_data where request_id = $request_id";
	}
	insert($statement);
	print $cgi->redirect("dailyActivity.cgi?featureRequest=developer");
	

}





