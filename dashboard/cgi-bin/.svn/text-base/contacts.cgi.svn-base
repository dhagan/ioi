#!/usr/bin/perl

################################################################################
#
#       File Name: contacts.cgi
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
#       02/09/2007      B. Scarborough  Modified to insure lowercase email addresses
################################################################################

use DBI;
use CGI;
use CGI qw(:standard escapeHTML);
use CGI::Carp "fatalsToBrowser";
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
my $dbh = getDBConnection();

$sth = $dbh->prepare("Select comp_name,comp_case_num from company order by comp_name");
$customer = $dbh->prepare("Select sub_name,sub_comp_link from users order by sub_name");
$customer->execute();
$sth->execute();
$cgi = new CGI;
if (param('update'))
{
	updateUser();
}
elsif (param('updateRes'))
{
	updateRes();
}
else { contactSearch(); }
sub updateUser()
{
	print $cgi->header();
	headers();
	print "<script language = 'javascript'>
	function checkSubmit()
	{
		if (document.form1.name.value == '')
		{
			alert ('Please enter a name');
			return false;
		}
		if (document.form1.email.value == '')
		{
			alert('Please enter an email address');
			return false;
		}
		if (document.form1.phone.value == '')
		{
			alert('Please enter a phone number');
			return false;
		}
		return true;
	}
	</script>";
	background();
	bodyAndLoad();
	### DJH $user = param('user');
	$user = getRemoteUser();
	$statement = "select sa_name,sa_phone,sa_cell_phone,sa_home_phone,sa_ichat,sa_e_mail,sa_street,sa_city,sa_state,sa_zip from staff where sa_e_mail = '$user'";
	($sa_name,$sa_phone,$sa_cell_phone,$sa_home_phone,$sa_ichat,$sa_e_mail,$sa_street,$sa_city,$sa_state,$sa_zip) = selectValues($statement);
	tableHead('65%');
	print "<form action ='' method = 'post' name='form1' onSubmit= 'return checkSubmit();'>
			<input type='hidden' name='updateRes' value='yes'>
			<input type='hidden' name='original' value='$user'>
		   <tr><td colspan='2'><center><b>Update profile for $sa_name</b></center></td></tr>
		   <tr><td>Name</td><td><input type='text' name='name' value='$sa_name'></td></tr>
		   <tr><td>Email</td><td><input type='text' name='email' value='$sa_e_mail'></td></tr>
		   <tr><td>iChat</td><td><input type='text' name='ichat' value='$sa_ichat'></td></tr>
		   <tr><td>Office Phone</td><td><input type='text' name='phone' value='$sa_phone'></td></tr>
		   <tr><td>Cell Phone</td><td><input type='text' name='cell_phone' value='$sa_cell_phone'></td></tr>
		   <tr><td>Home Phone</td><td><input type='text' name='home_phone' value='$sa_home_phone'></td></tr>
		   <tr><td>Address</td><td><input type='text' name='address' value='$sa_street'></td></tr>
		   <tr><td>City</td><td><input type='text' name='city' value='$sa_city'></td></tr>
		   <tr><td>State</td><td><input type='text' name='state' value='$sa_state'></td></tr>
		   <tr><td>Zip</td><td><input type='text' name='zip' value='$sa_zip'></td></tr>
		   <tr><td colspan = '2'><div align='center'><input type='submit' name='submit' value='Update'></div></td></tr>
		   </table></form>";
	end_html();
}
sub updateRes()
{
	$original = param('original');
	$name = param('name');
	$email = lc(param('email'));
	$ichat = param('ichat');
	$phone = param('phone');
	$cell_phone = param('cell_phone');
	$home_phone = param('home_phone');
	$address = param('address');
	$city = param('city');
	$state = param('state');
	$zip = param('zip');
	$name = quoteValues($name);
	$address = quoteValues($address);
	$statement = "update staff set sa_name= $name,sa_e_mail ='$email', sa_phone = '$phone', sa_home_phone ='$home_phone', sa_cell_phone = '$cell_phone',sa_ichat = '$ichat',sa_street = $address,sa_city = '$city',sa_state='$state',sa_zip = '$zip' where sa_e_mail = '$original'";
	#print $statement;
	insert($statement);
	print $cgi->redirect('contacts.cgi');
}
sub contactSearch
{
	print $cgi->header();
	print $cgi->start_html(-title=>"IOI Contacts");
	print"
	  <style type='text/css'>
	<!--
	body {
		background-color: #C0C0C0;
	}
	
	-->
	</style>
	
	</style><form name='form1' method='post' action='contactsResult.cgi'>
	  <p align='center'>IOI Contact Lookup </p>
	  <table width='80%'  border='1' align='center' cellpadding='5' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
		<tr>
		  <td width='18%'><strong>Customer</strong></td>
		  <td width='82%'><div align='center'>
			<input name='customer' type='text' id='customer' size='30'>  
			<select name='customer_select'>
			  <option value = ''></option>";
		   $array_ref2 = $customer->fetchall_arrayref( );
		foreach my $row (@$array_ref2)
		{
			my ($sub_name, $sub_comp_link) = @$row;
			print "<option value ='$sub_name'>$sub_name</option>\n";
		}
	 print"
			</select>
		  </div>
		</tr>
		<tr>
		  <td><strong>Company</strong></td>
		  <td><!--<input name='company' type='text' id='company'></td><td>-->
			<div align='center'>
			  <select name='company_select'>
		<option value = '' name = ''></option>";
		 $array_ref = $sth->fetchall_arrayref( );
		foreach my $row (@$array_ref)
		{
			my ($comp_name, $comp_case_num) = @$row;
			print "<option value ='$comp_case_num'>$comp_name</option>\n";
		}
	   print"
			  </select>
			</div>
		</tr>
	  </table>
	  <div align='center'>
		<input name='Submit' type='submit' id='Submit' value='Find'> 
		<input type='reset' name='Reset' value='Reset'>
	  </div>
	</form>";
	$sth = $dbh->prepare("select sa_name,sa_e_mail,sa_phone,sa_cell_phone,sa_ichat,sa_home_phone,sa_street,sa_city,sa_state,sa_zip from staff where sa_name <> 'Administrator' and sa_name <> 'CURRENTLY UNASSIGNED' and sa_name <> 'support' order by sa_name");
	$sth->execute();
	print"<table width='95%'  border='1' align='center' cellpadding='3' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'><tr>
	  <td><b>Name</b></td><td><b>Phone #</b></td><td><b>Email</b></td><td><b>Cell</b></td><td><b>Home Phone</b></td><td><b>iChat</b></td><td><b>Address</b></td></tr>";
	  $bgcolor = "#FF9900";
	  $bgcolor2 = '#B0B0B0';
	  $blue = 0;
	while(($sa_name,$sa_e_mail,$sa_phone,$sa_cell,$sa_ichat,$sa_home,$sa_street,$sa_city,$sa_state,$sa_zip) = $sth->fetchrow_array())
	{	
		if ($blue == 1) {$color = $bgcolor; $blue=0;} else {$color = $bgcolor2; $blue=0;}
		
		print "<tr  bgcolor=$color><td><b><a href='contacts.cgi?update=yes&user=$sa_e_mail'>$sa_name</a></b></td><td><b>$sa_phone</b></td><td><b>$sa_e_mail</b></td><td><b>$sa_cell</b></td><td><b>$sa_home</b></td><td><b>$sa_ichat</b></td><td><b>$sa_street $sa_city, $sa_state $sa_zip</b></td></tr>";
	}
	
	
	
	
	print"</table></body></html>";
}
