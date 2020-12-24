#!/usr/bin/perl

################################################################################
#
#       File Name: ticketSubmit.cgi
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

my $dbh = getDBConnection();

$cgi = new CGI;
print $cgi->header();

$submitted_by = $cgi->param('sub_login');
$sub_login = $submitted_by;
$comp_case_num = $cgi->param('sub_comp_link');
$customer = $cgi->param('customer');
$newCustomer = $cgi->param('createCustomer');
$newCompany = $cgi->param('createCompany');
$comp_name = $cgi->param('comp_name');
headers();
menu_focus();

background();
$user = getRemoteUser();
$sth = $dbh->prepare("select sa_e_mail from staff where sa_login ='$user'");
$sth->execute();
$staffEmail = $sth->fetchrow_array();
bodyAndLoad("menu_focus(document.form1.inputBy,\"$staffEmail\")");



$sth = $dbh->prepare("select sa_dept,sa_login from staff where sa_login like '$user'");
$sth->execute();
($dept,$user) = $sth->fetchrow_array();
if ($dept ne "IT")
{
	if ($newCustomer ne "" or $newCompany ne "")
	{
		if ($newCustomer ne "")
		{
		print "<body><form name='form1' action = 'ticketSubmitRes.cgi'>
		<input type='hidden' name='newCustomer' value='true'>";
		tableHead('95%');
		print"
		  <tr>
			<th width='50%' scope='row'><b>Customer Name</b></th>
			<td width='50%'><div align='center'>
				<input name = 'name' type = 'text' />
			</div></td>
		  </tr>    
		  <tr>
			<th scope='row'>Phone</th>
			<td><div align='center'>
			  <input name='phone' type='text' id='phone' />
			</div></td>
		  </tr>
		  <tr>
			<th scope='row'><b>Company</b></th>
			<td><div align='center'>
				<select name='company' class='textbox'>
				  <option value =''></option>";
				  $sth = $dbh->prepare("Select comp_name,comp_case_num from company order by comp_name");
		$sth->execute();
		$array_ref = $sth->fetchall_arrayref( );
		foreach my $row (@$array_ref)
			{
				my ($comp_name, $comp_case_num) = @$row;
				print "<option value ='$comp_name'>$comp_name</option>\n";
			}              
	print "              
				</select>
			</div></td>
		  </tr>
	
		  <tr>
			<th scope='row'><b>Subject:</b></th><td>
			<div align='center'>
			  <input name='subject' type = 'text' size='50' />
			</div></td>
		  </tr>
		  <tr>
			<th scope='row' colspan='2'><b>Problem:</b></th>
		  </tr>
		  <tr>
			<th scope='row' colspan='2'><textarea name='problem' rows='10' cols='100' ></textarea></th>
		  </tr>
		  <tr>
			<th scope='row'>Message Taken By:</th>
			  <td><select name='inputBy'><option value=''></option>";
		  $sth = $dbh->prepare("select sa_name,sa_e_mail from staff where sa_access <> 'Disabled' order by sa_name");
		  $sth->execute();
		  while(($sa_name,$sa_email) = $sth->fetchrow_array())
		  {
			print" <option value='$sa_email'>$sa_name</option>";
		  }
		  print "</select></td>
		  </tr>
		</table>
	  <p align='center'>
		<input type='submit' name ='submit' /> 
	</form>";
		}
		else 
		{
		print"<form name='form1' action = 'ticketSubmitRes.cgi'>
		<input type='hidden' name = 'newCompany' value='true'>
		<table width='80%'  border='1' cellpadding='3' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
		  <tr>
			<th width='25%' scope='row'><b>Customer Name</b></th>
			<td width='75%'><input type = 'text' name = 'name' /></td>
		  </tr>
		  <tr>
			<th scope='row'><b>Company</b></th>
			<td><input type='text' name='company' /></td>
		  </tr>
		  <tr>
			<th scope='row'>Phone # </th>
			<td><input name='phone' type='text' id='phone' /></td>
		  </tr>
		  <tr>
			<th scope='row'><b>Subject:</b></th>
			<td><input type = 'text' name='subject' size='50' /></td>
		  </tr>
		  <tr>
			<th scope='row' colspan='2'>Problem:</th>
		  </tr>
		  <tr>
			<th scope='row' colspan='2'><textarea name='problem' rows='10' cols='100'></textarea></th>
		  </tr>
		  <tr>
			<th scope='row'>Message Taken By</th>
			   <td><select name='inputBy'><option value=''></option>";
		  $sth = $dbh->prepare("select sa_name,sa_e_mail from staff where sa_access <> 'Disabled' order by sa_name");
		  $sth->execute();
		  while(($sa_name,$sa_email) = $sth->fetchrow_array())
		  {
			print" <option value='$sa_email'>$sa_name</option>";
		  }
		  print "</select></td>
		  </tr>
		</table>
		<p align='center'><input type='submit' name ='submit'>
	</form></body></html>";
		
	  }
	}
	else{
	
	
	
	my $dbh = getDBConnection();
	$sth = $dbh->prepare("select sub_name,sub_phone,sub_comp_link from users where sub_login = '$submitted_by'");
	$sth->execute();
	($sub_name,$sub_phone,$sub_comp_link) = $sth->fetchrow_array();
	print"<form name='form1' action = 'ticketSubmitRes.cgi' method='post'><center>
	<input type ='hidden' name='comp_name' value='$comp_name'>
	<input type='hidden' name='prob_comp_link' value = '$comp_case_num'>
	<input type='hidden' name='phone' value ='$sub_phone'>
	<input type = 'hidden' name='submitted_by' value = '$submitted_by'><input type = 'hidden' name='name' value = '$sub_name' />
	  <table width='80%'  border='1' cellpadding='3' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
		<tr>
		  <th width='50%' scope='row'>Company</th>
		  <td width='50%'>$comp_name</td>
		</tr>
		<tr>
		  <th scope='row'>Name</th>
		  <td>$sub_name</td>
		</tr>
		<tr>
		  <th scope='row'>Phone # </th>
		  <td>$sub_phone</td>
		</tr>
		 <tr>
		  <th scope='row'>Product</th>
		  <td><select name = 'prod_case_num'>";
		  $i=0;
	$sth = $dbh->prepare("select prod_name, prod_case_num from product where prod_comp_link = '$comp_case_num' ");
	$sth->execute;
	while (($prod_name,$prod_case_num) = $sth->fetchrow_array)
	{
		print "<option value = '$prod_case_num'>$prod_name</option>";
	}
		  
		  print"<option value = 'P1'>Other</option></select></td>
		</tr>
		<tr>
		  <th scope='row'>Subject</th>
		  <td><input type='text' size ='50' name='subject' /></td>
		</tr>
		<tr>
		  <th scope='row' colspan='2'><b>Problem:</b></th>
		</tr>
		<tr>
		  <th scope='row' colspan='2'><textarea name='problem' rows='10' cols='100'></textarea></th>
		</tr>
		<tr>
		  <th scope='row'> Message Taken By:      </th>
		  <td><select name='inputBy' onChange='updateAppendForm()'><option value=''></option>";
		  $sth = $dbh->prepare("select sa_name,sa_e_mail from staff where sa_access <> 'Disabled' order by sa_name");
		  $sth->execute();
		  while(($sa_name,$sa_email) = $sth->fetchrow_array())
		  {
			print" <option value='$sa_email'>$sa_name</option>";
		  }
		  print "</select>
		  </td>
		</tr>
	  </table>
	  <p align='center'><input type='submit' name ='submit'>
	</form>";
	activeTickets('staffAppend.cgi');
}
}
elsif ($dept eq "IT")
{
	activeTickets('respondTicket.cgi');
	print "<p><div align='center'><form name='form1' action='techSubmit.cgi' id='form1' method='get'>
	<input type='hidden' name='user' value='$user'>
	<input type='hidden' name='customer' value='$sub_login'>
	<input type='submit' name='submit' value='Create New Ticket'>
	</div>
	</form>";
}
	
	


sub activeTickets()
{
	$formselect = $_[0];
	print "<center>Currently Active Tickets for $comp_name</center>";
	$statement = $dbh->prepare("select case_num,short_desc,submitted_by,assigned_to,time_mod,date_mod,status from problem where prob_comp_link = '$comp_case_num' and status <> 'Closed' and status <> 'Awaiting Feature Request' and status <> 'Awaiting Bug Fix' order by submitted_by");
	$statement->execute();
	print "<table width='100%'  border='1' align='center' cellpadding='5' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>";
	print "<tr><th><strong>Case Number</th><th>Description</th><th>Assigned To</th><th>Last Modified</th><th>Status</th><th>Submitted By</th><th>Select</th></tr>";
	$form = 2;
	while(($case_num,$short_desc,$submitted_by,$assigned_to,$time_mod,$date_mod,$status ) = $statement->fetchrow_array())
	{
		$date_mod =~ s/00:00:00//g;
		$sth = $dbh->prepare("select sub_name from users where sub_login = '$submitted_by'");
		$sth->execute();
		$sub_name = $sth->fetchrow_array();
		#$user = $dbh->prepare("select sub_name from users where sub_login = '$submitted_by'");
		#$user->execute();
		#$sub_name = $user->fetchrow_array();
		print "<tr><form name='form$form' id='form$form' action='$formselect' method='post'><input type='hidden' name='inputBy' value=''><input type = 'hidden' name='case_num' value='$case_num'><input type = 'hidden' name='submitted_by' value='$submitted_by'>
		<input type = 'hidden' name='short_desc' value='$short_desc'><input type='hidden' name='user' value='$user'>
		<td><a href='respondTicket.cgi?viewTicket=true&case_num=$case_num'>$case_num</a></td><td>$short_desc</td><td>$assigned_to</td><td>$time_mod $date_mod</td>
		<td>$status</td><td>$sub_name</td><td><input type = 'submit' name='submit' value='Append'></td></form></tr>";
		$form++;
	}
	print "</table><script language='JavaScript' type='text/JavaScript'>
	function updateAppendForm()
	{ 
	";
	for ($i =2; $i< $form; $i++)
	{
	print "
	document.form$i.inputBy.value = document.form1.inputBy.value;";
	}
	print" 
	} </script>";
}
print $cgi->end_html();

