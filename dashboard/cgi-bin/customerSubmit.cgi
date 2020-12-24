#!/usr/bin/perl

################################################################################
#
#       File Name: customerSubmit.cgi
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

#customerSubmit.cgi
use DBI;
use CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
print $cgi->header();
$name = $cgi->param('name');
$login = $cgi->param('login');
$userpass = $cgi->param('password');
$confirm_password = $cgi->param('confirm_password');
$email = $cgi->param('email');
$phone = $cgi->param('phone');
$cell = $cgi->param('cell');
$department = $cgi->param('department');
$company = $cgi->param('company');
$notes = $cgi->param('notes');
$submit = $cgi->param('Submit');
$invalid = $cgi->param('invalid');
$company = $cgi->param('company');

headers();
my $dbh = getDBConnection();
menu_focus();
background();
print "
<script language = 'javascript'>
function checkSubmit()
{
	if (document.form1.password.value != document.form1.confirm_password.value)
	{
		alert('Passwords to not match');
		return false;
	}
	if (document.form1.name.value == '')
	{
		alert('Name is required');
		return false;
	}
	if (document.form1.login.value =='')
	{
		alert('Login name required');
		return false;
	}
	if (document.form1.company.value == '')
	{
		alert('Please choose a company for this customer');
		return false;	
	}
	if (document.form1.email.value =='')
	{
		alert('Please enter an email address for this customer');
		return false;
	}
	if (document.form1.phone.value =='')
	{
		alert('Please enter a phone number for this customer');
		return false;
	}
	return true;

}
function setup()
{
	menu_focus(document.form1.company,\"$company\");
}
</script>";
bodyAndLoad('setup()');
if ($login ne "")
{
	$sth = $dbh->prepare("select sub_login from users where sub_login = '$login'");
	$sth->execute();
	$checkLogin = $sth->fetchrow_array();
	if ($checkLogin ne "")
	{
		print "<script language ='javascript'> location.replace('customerSubmit.cgi?invalid=yes')</script>";
		
	}
}
	
if ($submit eq "")
{
print"
<form name='form1' id='form1' action='customerSubmit.cgi' method='get' onSubmit='return checkSubmit()'>
<div align='center'>";
if ($invalid ne "")
{
	print "This username is already taken by another customer, please select a new username.";
}
print"	
  <table width='81%' height='72'  border='1' cellpadding='0' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090'>
    <tr>
      <td width='49%'><div align='center'>Company</div></td>
      <td width='51%'><div align='center'>
        <select name='company'><option value=''></option>";
        $sth = $dbh->prepare("select comp_phone from company where comp_case_num='$company'");
        $sth->execute();
        $comp_phone = $sth->fetchrow_array();
        $sth = $dbh->prepare("select comp_name,comp_case_num from company order by comp_name");
        $sth->execute();
        while(($comp_name,$comp_case_num) = $sth->fetchrow_array())
        {
        	print "<option value='$comp_case_num'>$comp_name</option>";
        }
       
       print"
        </select>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Name</div></td>
      <td><div align='center'>
        <input name='name' type='text' id='name'>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Login Name </div></td>
      <td><div align='center'>
        <input name='login' type='text' id='login'>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Password</div></td>
      <td><div align='center'>
        <input name='password' type='password' id='password' value='ioi'>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Confirm Password </div></td>
      <td><div align='center'>
        <input name='confirm_password' type='password' id='confirm_password' value='ioi'>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Email</div></td>
      <td><div align='center'>
        <input name='email' type='text' id='email'>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Phone</div></td>
      <td><div align='right'>
        <input name='phone' type='text' id='phone' value='$comp_phone'>Default:Company Phone
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Cell</div></td>
      <td><div align='center'>
        <input name='cell' type='text' id='cell'>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Department</div></td>
      <td><div align='center'>
        <input type='text' name='department'>
      </div></td>
    </tr>
    <tr>
      <td><div align='center'>Notes</div></td>
      <td><div align='center'>
        <textarea name='notes' cols='50' rows='6' id='notes'></textarea>
      </div></td>
    </tr>
  </table>
<input type='submit' name='Submit' value='Submit'>
    <input type='submit' name='Submit' value='Reset'>
</div>
</form>
<div align ='center'>If there is no company for this customer click <a href='companySubmit.html'>here</a> to create a new company</div>
</body>
</html>'";
}
elsif ($submit eq "Submit")
{
	$sth = $dbh->prepare("select max(id_num) from users");
	$sth->execute();
	$id_num = $sth->fetchrow_array();
	$id_num++;
	$name = $dbh->quote($name);
	$login = $dbh->quote($login);
	$userpass = $dbh->quote($userpass);
	$email = $dbh->quote($email);
	$phone = $dbh->quote($phone);
	$cell = $dbh->quote($cell);
	$department = $dbh->quote($department);
	$company = $dbh->quote($company);
	$notes = $dbh->quote($notes);
	$statement = "insert into users (id_num,sub_login,sub_name,sub_password,sub_e_mail,sub_phone,cell_phone,sub_dept,sub_notes,sub_access,sub_comp_link) values ('$id_num',$login,$name,$userpass,$email,$phone,$cell,$department,$notes,'Active',$company)";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	$dbh->commit();
	$dbh->disconnect();
	print "<div align='center'>$name has been successfully submitted to the helpdesk. Click <a href ='customerSubmit.cgi'>here</a> to add another customer";
	print $cgi->end_html();
}