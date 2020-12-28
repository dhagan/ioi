#!/usr/bin/perl

################################################################################
#
#       File Name: respondTicket.cgi
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
#       02/09/2007      B. Scarborough  Modified respondTicket() to add view Product info button
#       03/29/2007      B. Scarborough  Modified respondTicket() to add generic sendMail function
################################################################################

use CGI;
use DBI;
use CGI::Carp qw(fatalsToBrowser);
use File::Find::Rule;
use File::stat;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";

my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 1000000; 
$cgi = new CGI;

my $mycookie = 'ioidashboard';

($sub_e_mail, $sub_name, $sub_comp_link) = &getUserSession();
if (!$sub_e_mail || !$sub_name || !$sub_comp_link) {
   print $cgi->header();
   print "You appear to be logged out, please login";
   print "<input id='login' type='button' value='Login' onclick=\"window.location='hd-login.cgi'\"/>";
   exit;
}

use CGI qw(:standard escapeHTML);

if (param('viewTicket'))
{
	getTicketInfo();
	viewTicket();
}
elsif (param('newuser'))
{
	newUser() if (param('newuser') eq "yes");
	newUserRes() if (param('newuser') eq "update");
}
else 
{
	getTicketInfo();
	respondTicket(); 
}

sub newUser()
{
	my $submitted_by = param('submitted_by');
	my $case_num = param('case_num');
 	#my $user = param('user');
	### DJH 10/26/2010
	$user = getRemoteUser();
 	$statement = "SELECT sub_name,sub_e_mail,sub_phone FROM users WHERE sub_login = '$submitted_by'";
 	(my $sub_name,my $sub_email,my $sub_phone) = selectValues($statement);
 	print $cgi->header();
 	headers();
 	menu_focus();
 	print "<script language='javascript'>
 	function checkSubmit(state)
 	{
 		if (state == 'Assign' && document.assignUser.sub_login.value == '')
 		{
 			alert('You must choose a customer to assign this to.');
 			return false;
 		}
 		if (state == 'Create User' && document.assignUser.company.value == '')
 		{
 			alert('You must choose a company to add this user to');
 			return false;
 		}
		else
		{
			//document.assignUser.submit();
			return true;
		}
 	}
 	</script>";
 	background();
 	bodyAndLoad("menu_focus(document.assignUser.assigned_to,\"$user\")");
 	ioiFont("This user '$submitted_by' is a new user in the database, please select a company to assign them to and fill out their information or select an alternate user to assign this ticket to.<p>");

 	tableHead('65%');
 	print "<form name='assignUser' action='changeUser.cgi' id='assignUser'>
 	<input type='hidden' name='old_user' value = '$submitted_by'>
 	<input type='hidden' name='case_num' value='$case_num'>";
 	print "<tr><td>Assign To</td><td colspan = '2'>";
 	techDropDown();
 	print "</td></tr><tr><td>Select Customer to assign this ticket to</td><td>";
 	customerDropDown();
 	print "</td><td><input type='submit' name='submit' value='Assign' onClick='return checkSubmit(this.value)'></td></tr><tr><td>Create new customer with existing company</td><td>";
 	companyDropDown();
 	print "</td><td><input type='submit' name='submit' value='Create User' onClick='return checkSubmit(this.value)'></td></tr><tr><td>Create new customer and new company</td><td colspan ='2'>
 	<input type='submit' name='submit' value='Create User and Company' onClick ='return checkSubmit(this.value)'>
 	</td></tr></form></table>";
 	ioiFont("Current Ticket Info<p>");
	getTicketInfo("viewTicket");
 	viewTicket(1);
 	end_HTML();
 }

sub viewTicket()
{
	$user = getRemoteUser();
	$newUser = $_[0] if ($_[0]);
	headers();
	print "<script language ='javascript'>
	function checkUser()
	{
		if (document.form1.assigned_to.value == '')
		{
			alert('You must choose a tech to assign this ticket to');
			return false;
		}
		return true;
	}
	</script>";
	menu_focus();
	background();
	if (!$newUser)
	{
		tableHead('30%');
		print "<form name='form1' id='form1' action='assignTickets.cgi' onSubmit='return checkUser();'>
		<input type='hidden' name='case_num' value='$case_num'>
		<input type='hidden' name='notnew' value='yes'>
		<tr><td>Assign To</td><td>";
		techDropDown();
		print "</td><td><input type='submit' name='submit' value='Assign To Tech'></td></tr><tr><td colspan='3'>
		<input type='submit' name='submit' value='Assign to me and update' onClick='menu_focus(document.form1.assigned_to,\"$user\")'></td></tr></table>";
	}	
	tableHead('90%');
	smallFont();
	print "<tr><td><div align='left'>Name: <strong>$sub_name</strong></div></td><td><div align='left'>Email: <strong>$sub_email</strong><div></td><td><dilv align='left'>Phone: <strong>$sub_phone</strong></div></td></tr>
	<tr><tr><td><div align='left'><strong>Company: $comp_name</strong></div></td>
	<td><div align='left'>Billing Address: <strong>$comp_bill_address $comp_bill_state,$comp_bill_zip</strong></div></td>
	<td><div align='left'>Status: <strong>$status</strong></div></td>
	<tr><td><div align='left'>Product:<b>$prod_name</b></div></td><td><div align='left'>Serial # <b>$prod_part_num</b></div></td><td><div align='left'>Assigned To: <strong>$assigned_to</strong></div></td></tr>
	<tr><td><div align='left'>Vendor Ticket # <b>$ticket</b></td><td colspan = '1'><div align='left'>Subject: <strong>$short_desc</strong></div></td><td></td></tr></table>";
	tableHead('90%');
	splitProblem(param('order'));
	print "</table>";
	end_HTML();
}




sub respondTicket()
{
	$sth = $dbh->prepare("UPDATE problems set allow_submit = 1 WHERE case_num = '$case_num'");
	$sth->execute();
	$dbh->commit();

#	if ($assigned_to eq "nobody")
#	{
#		$status = "Assigned";
#		$assigned_to = "$user";
#		$sth = $dbh->prepare("UPDATE problems set status = '$status', assigned_to = '$assigned_to' WHERE case_num = '$case_num'");
#		$sth->execute();
#		$dbh->commit();
#		$email_body = "This ticket has now been assigned to $user. Your ticket number for reference is $case_num";
#                sendMail("techs\@iointegration.com", "Ticket $case_num, '$short_desc' has been assigned to $user", $email_body);
#	}
#	
#	if (lc($assigned_to) ne lc($user) and $confirmUpdate ne "true")
#	{
#		print "
#		<meta name=\"viewport\" content=\"width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;\"/>
#		<style type='text/css'>
#		<!--
#		body {
#		background-color: #C0C0C0; width: auto;
#		}
#		-->
#	</style>
#
#		<div align='left'><font color = '#000000'>This ticket is currently assigned to $assigned_to, are you sure you want to update?</font><p>
#		<form action = 'respondTicket.cgi' name='form1' method='post'>
#		<input type='hidden' name='confirmUpdate' value='true'>
#		<input type='hidden' name='user' value='$user'>
#		<input type='hidden' name='case_num' value='$case_num'>
#		<input type='submit' name='submit' value='Continue'>
#		<input type='button' name='Cancel' value='Cancel' onClick='javascript:location.replace(\"http://dashboard.iointegration.com/dashboard/thankYou.cgi\")'>
#		</form>
#		</body>
#		</html>";
#	}
#	else

	{
	
	print "
	
	<html>
	<meta name=\"viewport\" content=\"width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;\"/>

	<head>
	<title>Ticket Update</title>
	<style type='text/css'>
	<!--
	body {
		background-color: #C0C0C0; width: auto;
	}
	body,td,th {
		font-size: 12 px;
	}
	-->
	</style>
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
--></style>
	</head>";
if ($special_instructions) {;
	print "<script src='http://code.jquery.com/jquery-latest.min.js'></script>
	<script src='/jquery-blink.js' language='javscript' type='text/javascript'></script>
	<script type='text/javascript' language='javascript'>
	\$(document).ready(function()
	{
		\$('.blink').blink(); // default is 500ms blink interval.
		//$('.blink').blink({delay:100}); // causes a 100ms blink interval.
	});
	</script>";
}

	print "<script type='text/javascript'><!--
	function setup()
	{
		menu_focus(document.form1.product,'$prob_prod_link');
		menu_focus(document.form1.status,'$status');
		menu_focus(document.form1.assigned_to,'$assigned_to');
		menu_focus(document.form1.priority,'$priority_type');
	}
	
	function menu_focus(el,val)
	{
			var j;
			var el_length;
			el_length=el.length;
			for(j=0; j< el_length;j++)
			{
			  if(el.options[j].value==val)
				{
				  el.selectedIndex=j;
				 }
			 }
	}
	function checkAssign(element,thisAssign)
	{
		if ( element != 'Nige')
		{
			var checkAssignment = confirm('This ticket is assigned to $assigned_to, are you sure you want to change it to ' + element);
			if (checkAssignment == true)
			{
			}
			else 
			{ 		
			menu_focus(document.form1.assigned_to,'$assigned_to');
			}
		}
	}
	function submitCheck()
	{
		if (document.form1.problem.value == 0)
		{
			alert('Please state the problem.');
			return false;
		}
//		if (document.form1.time_spent.value >= 1000)
//		{	
//					
//			var checkOver = confirm('This time spent value is too high, if this was meant to be the vendor ticket number click yes');
//			if (checkOver == true)
//			{
//				document.form1.xinet_ticket_num.value = document.form1.time_spent.value;
//			}
//			document.form1.time_spent.value = '';
//			return false;
//		}
//		if (document.form1.priority.value == '')
//		{
//			alert('Please set a priority');
//			return false;
//		}
//					
//					
//		if(document.form1.status.value == 'Open' || document.form1.status.value == 'Assigned')
//		{
//					alert('Please choose a Pending State');
//					return false;
//		}	
//		var time_already_spent = $time_spent;
//		var time_spent = document.form1.time_spent.value;
//		time_spent = parseInt(time_already_spent) + parseInt(time_spent);
//		document.form1.time_spent.value = time_spent;
		return true;
	
	}
	function formOnClick(thisAction)
	{
//		if (thisAction == \"vendor\")
//		{
//			document.form1.email_action.value = 'Email Vendor';
//		}
//		if (thisAction == \"client\")
//		{
//			document.form1.email_action.value = 'Email Client';
//		}
//        if (thisAction == \"techs\")
//		{
//			document.form1.email_action.value = 'Email';
//		}
		if (thisAction == \"none\")
		{
			document.form1.email_action.value= 'Submit';
		}
	}
	
	//-->
	</script>
	<body onLoad ='setup()'>
	<style type='text/css'>
	<!--
	body {
		background-color: #ffffff; width: auto; margin: 25px;
	}
	-->
	</style>

<div style=\"float: right;\" width='100px'>
<input id='helpdesk' type='button' value='Active Tickets' onclick=\"window.location='helpdesk.cgi'\"/>&nbsp;&nbsp;
<input id='logout' type='button' value='Logout' onclick=\"window.location='hd-logout.cgi'\"/>
<p>
</div>

	<div align='left'>
	<FORM NAME ='form1' ACTION=\"hd-email2.cgi\" METHOD=\"POST\" ENCTYPE=\"multipart/form-data\" onSubmit= 'return submitCheck()'>
	  <input type = 'hidden' name='user' value='$user'>
	  <input type='hidden' name='email_action'>
	  <input type= 'hidden' name='link' value = 'hd-respondTicket.cgi?case_num=$case_num&user=$user'>
	  <input type= 'hidden' name='case_num' value='$case_num'>
	  <input type= 'hidden' name='sub_name' value='$sub_name'>
	  <input type= 'hidden' name='sub_email' value='$sub_email'>
	  <input type= 'hidden' name='status' value='$status'>
	  <input type= 'hidden' name='short_desc' value='$short_desc'>
	  <input type= 'hidden' name='problem' value='$problem'>
	  <input type= 'hidden' name='assigned_to' value='$assigned_to'>";
	  print "
	  	<input type='hidden' name='comp_case_num' value='$comp_case_num'>
		<table width='100%' height='425'  border='1' cellpadding='1' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#f5f5f5'>
                  <tr>
			<td colspan='2'><div align='left'><strong>Subject:</strong> $short_desc</div></td>
		  </tr>
                  <tr>
			<td width='21%'><div align='left'><strong>Ticket Number:</strong> $case_num </div></td>
			<td width='31%'><div align='left'><strong>Date Open: </strong> $date_open</div></td>
	          </tr>
                  <tr>
			<td width='22%'><div align='left'><strong>Product:</strong> $prod_name</div></td>
			<td width='26%'><div align='left'><strong>Status:</strong> $status</div></td>
		  </tr>
                  <tr>
			<td><div align='left'><strong>Priority:</strong> $priority_type</div></td>
			<td></td>
	          </tr>
                  <tr>
			<td colspan='2'><div align='left'><strong>Problem:</strong></div></td>
		  </tr>
                  <tr>
			<td colspan='2'><div align='left'>
			  <textarea name='problem' rows='16' style='width: 100%'>$mistake_problem"; 
	
			$link_desc = $short_desc;
			$link_desc =~ s/ /+/g;
			$link_desc =~ s/'/%20/g;
			  print"</textarea>
			<!--
			 <a href='knowledgebase.cgi?short_desc=$link_desc&free_text_query=Yes' target='_new'>Search Knowledgebase</a>
			-->
			</div></td>
		  </tr>
                  <tr>
			<td colspan='2'><div align='left'><strong>
				<input type='submit' name='button' value='Update Ticket' onClick='formOnClick(\"none\")'>
			</div></td>
		  </tr>
		</table>
		
	  <table width='100%'  border='1' cellpadding='0' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#f5f5f5'>
		<tr>
		  <td width='23%'><div align='left'>Activity</div></td>
		  <td width='77%'><div align='left'>
			<p>Problem</p>
			</div></td>
		</tr>";
		splitProblem(param('order'));
		print"
		<tr bgcolor='#f5f5f5'>
		  <td>&nbsp;</td>
		  <td>&nbsp;</td>
		</tr>
	  </table>
	  <table width='100%'  border='1' cellpadding='0' bordercolor='#C0C0C0' bgcolor='#f5f5f5'>
		<tr>
		  <td bgcolor='#f5f5f5'><div align='left'>Attachments</div></td>
		</tr>
		<tr>
		  <td><div align='left'>
			Attachment 1<input type='file' name='attachment1'>
		  </div></td>
		</tr>
		<tr>
		  <td><div align='left'>
			  Attachment 2<input type='file' name='attachment2'>
		  </div></td>
		</tr>
		<tr>
		  <td><div align='left'>Attachment 3
			  <input type='file' name='attachment3'>
		  </div></td>
		</tr>
		<tr><td><div align='left'><b>Current Attachments<b></div></td></tr><tr><td><div align='left'>";
		my @newfiles = File::Find::Rule->file()
									   ->name('*')
									   ->in("/var/www/html/workflow/uploadFileDir/dashboard/$case_num/");
		print "<table width ='50%' border ='1'><tr><td>Date</td><td>File</td></tr>";
		foreach $file(@newfiles)
		{
			$st = stat($file) or die "No $file: $!";
			(my $sec,my $min,my $hour,my $mday,my $mon,my $year,my $wday,my $yday,my $isdst) = localtime($st->mtime);
			$year += 1900;
			
			print "<td>$mon/$mday/$year at $hour:$min:$sec</td>";
			if ($file =~ /$case_num\//)
			{
				$filename = $';
			}
		
			print "<td><a target='new' href='http://dashboard.iointegration.com/uploadFileDir/dashboard/$case_num/$filename'>$filename</a> &nbsp;&nbsp;</td></tr>";
		}
		print "</table>";
	print "	
	  </div></td></tr></table>
	  <p>";
	  print"<input type='submit' name='button' value='Update Ticket' onClick='formOnClick(\"none\")'>
	</p>
	  </form>
	</div>
	</body>
	</html>
	";
	}
}

# sub newUser()
# {
# 	my $submitted_by = param('submitted_by');
# 	my $case_num = param('case_num');
# 	my $user = param('user');
# 	$statement = "select sub_name,sub_e_mail,sub_phone FROM users WHERE sub_login = '$submitted_by'";
# 	(my $sub_name,$sub_email,$sub_phone) = selectValues($statement);
# 	print $cgi->header();
# 	headers();
# 	print "<script language='javascript'>
# 	function checkSubmit()
#  	{
#  		if (document.form1.company.value == ''){ alert('Please choose a company for this contact'); return false;}
#  		if (document.form1.sub_name.value == ''){ alert('Please enter a name for this contact'); return false;}
#  		if (document.form1.sub_email.value ==''){alert('Please enter an email for this contact'); return false;}
#  		if (document.form1.sub_phone.value ==''){alert('Please enter a phone # for this contact'); return false;}
#  		if (document.form1.sub_login.value == ''){alert('Please enter a login for this contact'); return false;}
#  		if (document.form1.sub_password.value == ''){alert('Please enter a password for this contact'); return false;}
#  		if (document.form1.sub_access.value == 'Disabled')
#  		{ var checkdisable = confirm('Are you sure you want to disable this account');
#  			if (checkdisable == true)
#  			{
#  			}
#  			else
#  			{
#  				menu_focus(document.form1.sub_access,'Active');
#  				return false;
#  			}
#  			return true;
#  		}
#  	}
#  	function checkSubmitForm2()
#  	{
#  		if (document.form2.sub_login.value == '')
#  		{
#  			alert('Please select a user to assign this ticket to');
#  			return false;
#  		}
#  		if (document.form2.sub_login.value != '')
#  			var sub_login = document.form2.sub_login.value;
#  		{ 
#  			var checkdisable = confirm(\"This will delete $submitted_by do you want to continue?\");
#  			if (checkdisable == true)
#  			{
#  			}
#  			else
#  			{
#  				return false;
#  			}
#  		}
#  			return true;
#  	}
#  			
# 	</script>\n";
# 	background();
# 	bodyAndLoad();
# 	ioiFont("This user '$submitted_by' is a new user in the database, please select a company to assign them to and fill out their information or select an alternate user to assign this ticket to.<p>");
# 	print "<div align='left'>";
# 	print "<form name='form2' action='' onSubmit='return checkSubmitForm2()' id='form2'>
# 		<input type='hidden' name='newuser' value='update'><div align='left'>
# 		<input type='hidden' name='old_email' value='$sub_email'>
# 		<input type='hidden' name='append_to_contact' value='yes'>
# 		<input type='hidden' name='old_login' value='$submitted_by'>
# 		<input type='hidden' name='case_num' value='$case_num'>";
# 	ioiFont("<b>Select a contact to take over this users ticket</b> (This will delete '$submitted_by' as a user)\n");
# 	customerDropDown();
# 	print "</div><p><input type='submit' name='submit' value ='Assign to user'></form><p><p>";
# 	ioiFont("<b>OR fill out user information</b>");
# 	print "<left><font color='white'>This username is already taken, please select a new username</font></left>" if (param('duplicate_login'));
# 	print "<form name='form1' action='' onSubmit='return checkSubmit()' id='form1'>
# 	<input type='hidden' name='newuser' value='update'><div align='left'>
# 	<input type='hidden' name='old_email' value='$sub_email'>
# 	<input type='hidden' name='old_login' value='$submitted_by'>
# 	<input type='hidden' name='case_num' value='$case_num'>
# 	<input type='hidden' name='user' value='$user'>";
# 	
# 	tableHead('75%');
# 	print "<tr><td>Company</td><td>";
# 	companyDropDown();
# 	print "</td></tr>
# 	<tr><td>Name</td><td><input type='text' name='sub_name' value='$sub_name'></td></tr>
# 	<tr><td>Login</td><td><input type='text' name='sub_login' value='$submitted_by'></td></tr>
# 	<tr><td>Password</td><td><input type='password' name='sub_password' value='ioi'>(Default:ioi)</td></tr>
# 	<tr><td>Email</td><td><input type='text' name='sub_email' value='$sub_email'?</td></tr>
# 	<tr><td>Phone</td><td><input type='text' name='sub_phone' value='$sub_phone'></td></tr>
# 	<tr><td>Cell Phone</td><td><input type='text' name='sub_cell'></td></tr>
# 	<tr><td>Fax</td><td><input type='text' name='fax'></td></tr>
# 	 <tr><td>Access</td><td><select name='sub_access'><option value='Active'>Active</option><option value='Disabled'>Disabled</option></select></td></tr>
# 	<tr><td>Department</td><td><input type='text' name='sub_dept' value=''></td></tr>
# 	<tr><td>Notes</td><td><textarea name='sub_notes' rows='10' cols='60'></textarea></td></tr>
# 	<tr><td colspan='2'><div align='left'><input type='submit' name='submit' value='Update $submitted_by'></div></td></tr></table>";
# 	
# 	
# 	print "</left>";
# 	print "</form><p>";
# 	ioiFont("Current Ticket Info<p>");
# 	getTicketInfo("viewTicket");
# 	viewTicket();
# 	end_HTML;
# }

# sub newUserRes()
# {
# if (param('append_to_contact'))
# {	
# 	$old_login = param('old_login');
# 	$sub_login = param('sub_login');
# 	$case_num = param('case_num');
# 	print $cgi->header();
# 	background();
# 	bodyAndLoad();
# 	insert("UPDATE problems SET submitted_by = '$sub_login' WHERE submitted_by = '$old_login' AND case_num = '$case_num'");
# 	#sqlDelete("delete * FROM users WHERE sub_login = '$old_login'");
# 	ioiFont("The user $sub_login has now been assigned to $case_num.<p>Click <a href='http://dashboard.iointegration.com/respondTicket.cgi?case_num=$case_num&user=$user'>here</a> to update ticket $case_num.");
# 	end_HTML();
# }	
# else
# 	{
# 	my $dbh = getDBConnection();
# 	$dbh-> {'LongReadLen'} = 1000000;
# 	$sub_login = param('sub_login');
# 	$case_num = param('case_num');
# 	$sub_email = param('sub_email');
# 	$old_email = param('old_email');
# 	$old_login =param('old_login');
# 	$sth = $dbh->prepare("select sub_login FROM users WHERE sub_login = '$sub_login' and sub_e_mail <> '$old_email'");
# 	$sth->execute();
# 	$duplicateValue = $sth->fetchrow_array();
# 	print $cgi->redirect("respondTicket.cgi?submitted_by=$old_login&newuser=yes&duplicate_login=yes&case_num=$case_num&user=$user") if ($duplicateValue ne "");
# 	$sub_name = param('sub_name');
# 	$sub_phone = param('sub_phone');
# 	$cell_phone = param('cell_phone');
# 	$sub_fax = param('sub_fax');
# 	$sub_access = param('sub_access');
# 	$sub_dept = param('sub_dept');
# 	$sub_notes = param('sub_notes');
# 	$sub_password = param('sub_password');
# 	$sub_comp_link = param('company');
# 	$user = param('user');
# 	$sub_notes = quoteValues($sub_notes);
# 	$sub_email = quoteValues($sub_email);
# 	$sub_name = quoteValues($sub_name);
# 	insert("UPDATE users SET sub_name=$sub_name,sub_comp_link='$sub_comp_link',sub_e_mail=$sub_email,sub_phone='$sub_phone',sub_dept='$sub_dept',sub_notes = $sub_notes,cell_phone='$cell_phone',sub_fax='$sub_fax',
# 		   sub_access = '$sub_access',sub_password = '$sub_password' WHERE sub_login = '$old_login'");
# 	print $cgi->redirect("respondTicket.cgi?user=$user&case_num=$case_num");
# 	
	# print $cgi->header();
# 	headers();
# 	background();
# 	bodyAndLoad();
# 	ioiFont("'$sub_name' has been updated, click <a href='management.cgi?sub_login=$sub_login&contact=update'>here</a> to modify your recently updated contact.<p>Click <a href=''>here</a> to go back to the management page.");
# 	end_html();
#	}
#}

sub getTicketInfo()
{
	$newUserViewTicket = $_[0];
	$case_num= $cgi->param('case_num');
	### DJH 10/26/2010 $user = $cgi->param('user');
	### DJH 12/26/2020 $user = getRemoteUser();
	$mistake_problem = $cgi->param('problem');
	$staffmember = $cgi->param('staffmember');
	$confirmUpdate= $cgi->param('confirmUpdate');
	@searchText = $cgi->param('query');
	
	$statement = "SELECT short_desc,status,prob_prod_link,prob_comp_link,submitted_by,priority_type,date_open,time_spent,xinet_ticket_num,assigned_to,bug_ticket_num FROM problems WHERE case_num = '$case_num'";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	(($short_desc,$status,$prob_prod_link,$prob_comp_link,$submitted_by,$priority_type,$date_open,$time_spent,$ticket,$assigned_to,$bug_ticket_num) = $sth->fetchrow_array());
	if (param('query'))
	{
		foreach $word(@searchText)
		{
			$short_desc =~ s/$word/<b><font color='red'>$word<\/font><\/b>/gi;
			$problem =~ s/$word/<b><font color='red'>$word<\/font><\/b>/gi;
		}
	}
	$time_spent = 0 if ($time_spent eq "");
	$sth = $dbh->prepare("SELECT sub_comp_link FROM users WHERE sub_login = '$submitted_by'");
	$sth->execute();
	$sub_comp_link = $sth->fetchrow_array();
	
	$statement = "SELECT comp_bill_address,comp_bill_state,comp_bill_zip,comp_name,comp_case_num, special_instructions FROM company WHERE comp_case_num = '$sub_comp_link'";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	
	(($comp_bill_address,$comp_bill_state,$comp_bill_zip,$comp_name,$comp_case_num, $special_instructions) = $sth->fetchrow_array());
	
	$sth = $dbh->prepare("SELECT prod_name,prod_case_num,prod_part_num FROM product WHERE prod_comp_link = '$sub_comp_link'");
	$sth->execute();
	$prod = 0;
	while(($prod_name,$prod_case_num) = $sth->fetchrow_array())
	{ @prod_name[$prod] = $prod_name; @prod_case_num[$prod] = $prod_case_num; $prod++; } 
	$sth = $dbh->prepare("SELECT prod_part_num,prod_name FROM product WHERE prod_case_num = '$prob_prod_link'");
	$sth->execute();
	($prod_part_num,$prod_name) = $sth->fetchrow_array();
	$sth = $dbh->prepare("SELECT sub_name,sub_e_mail,sub_phone FROM users WHERE sub_login = '$submitted_by'");
	$sth->execute();
	($sub_name,$sub_email,$sub_phone) = $sth->fetchrow_array();
	$date_open =~ s/00:00:00//g;
	$submitted_by =~ s/ /+/g;
	print $cgi->redirect("hd-respondTicket.cgi?newuser=yes&submitted_by=$submitted_by&case_num=$case_num&user=$user") if ($sub_comp_link eq "COMP0" and $newUserViewTicket ne "viewTicket");
	print $cgi->header() if ($newUserViewTicket ne "viewTicket");
}
sub splitProblem
{
	my $order = $_[0];
	my $case_num= $cgi->param('case_num');
        my $is_customer = false;
        my $ordering = 'ASC';
        if ($order eq "newestTop") {
            print "<div align='left'><span class='toggle' onClick=\"parent.location='hd-respondTicket.cgi?user=$user&case_num=$case_num&order=oldestTop'\">Order oldest to newest</span></div>";
            $ordering = 'DESC';
        } else {
            print "<div align='left'><span class='toggle' onClick=\"parent.location='hd-respondTicket.cgi?user=$user&case_num=$case_num&order=newestTop'\">Order newest to oldest</span></div></div>";
            $ordering = 'ASC';
        }

        my $query = "SELECT d.description, d.description_updated_by, d.status, d.action, d.created FROM descriptions d JOIN problems p ON p.id = d.problem_id WHERE p.case_num = '$case_num' ORDER BY d.created $ordering"; 
        $sth = $dbh->prepare($query);
        $sth->execute();
        my $return = '';
        
        while ((my $description, my $description_updated_by, my $status, my $action, my $created) = $sth->fetchrow_array())
        {
            print"
	    <tr>
              <td><p>Who: $description_updated_by</p>
              <p>When: $created</p>
              <p>Action: $action</p>
              <p>Status: $status</p></td>
              <td>$description</td>
            </tr>";
	}	
}
