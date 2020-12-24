#!/usr/bin/perl

################################################################################
#
#       File Name: changeUser.cgi
#
#       Purpose: This file is intended to allow an IOI tech member to update a
#                ticket that is submitted by a customer that is not yet in the
#                database. It will allow them to assign to another user,create a
#                new user, or create a new user and a new company. 
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       11/09/2005      M. Smith        Created this file
#       02/09/2007      B. Scarborough  Modified to insure lowercase email addresses
################################################################################

use CGI qw(:standard escapeHTML);
use CGI::Carp qw(fatalsToBrowser);
use DBI;
use MIME::Lite;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
### First lets find what state we are in ###	
if (param('submit'))
{
	changeUser() if (param('submit') eq "Assign");
	newUser() if (param('submit') eq "Create User");
	newUserComp() if (param('submit') eq "Create User and Company");
	assignTech() if (param('submit') eq "Assign To Tech");
	assignMe() if (param('submit') eq "Assign to me and update");
}
if (param('result'))
{
	newUserRes() if (param('result') eq "Create User");
	newUserCompRes() if (param('result') eq "Create User and Company");
}

sub changeUser()
{
	my $old_user = param('old_user');
	my $new_user = param('sub_login');
	my $case_num = param('case_num');
	my $assigned_to = param('assigned_to');
	print $cgi->header();
	background();
	bodyAndLoad();
	my $statement = "update problem set submitted_by = '$new_user',assigned_to = '$assigned_to' where submitted_by = '$old_user' and case_num = '$case_num'";
	insert($statement);
	#sqlDelete("delete * from users where sub_login = '$old_login'");
	ioiFont("The user $new_user has now been assigned to $case_num.<p>This ticket has been assigned to $assigned_to.<p>Click <a href='http://dashboard.iointegration.com/dashboard/respondTicket.cgi?case_num=$case_num&user=$assigned_to'>here</a> to update ticket $case_num.");
	end_HTML();
}
sub assignTech()
{
	my $assigned_to = param('assigned_to');
	my $case_num = param('case_num');
	my $statement = "update problem set assigned_to = '$assigned_to' where case_num = '$case_num'";
	insert($statement);
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	ioiFont("Ticket $case_num has been assigned to $assigned_to");
	END_HTML;
}
sub assignMe()
{
	my $assigned_to = param('assigned_to');
	my $case_num = param('case_num');
	my $statement = "update problem set assigned_to = '$assigned_to',status='Pending IOI' where case_num = '$case_num'";
	insert($statement);
	print $cgi->redirect("respondTicket.cgi?case_num=$case_num&user=$assigned_to");
}
sub newUser()
{
	my $case_num = param('case_num');
	my $assigned_to = param('assigned_to');
	my $old_user = param('old_user');
	my $company = param('company');
	my $error = param('error');
	print $cgi->header();
	if ($old_user ne "VENDOR_EMAIL")
	{	
		($sub_name,$sub_login,$sub_email) = selectValues("select sub_name,sub_login,sub_e_mail from users where sub_login = '$old_user'");
	}
	headers();
	menu_focus();
	background();
	bodyAndLoad("menu_focus(document.form1.company,\"$company\")");
	
	ioiFont("This ticket will be assigned to $assigned_to upon submittal");
	print "<script language='javascript'>

 	function checkSubmit()
 	{
 		if (document.form1.sub_name.value == ''){ alert('Please enter a name for this contact'); return false;}
 		if (document.form1.sub_email.value ==''){alert('Please enter an email for this contact'); return false;}
 		if (document.form1.sub_phone.value ==''){alert('Please enter a phone # for this contact'); return false;}
 		if (document.form1.sub_login.value == ''){alert('Please enter a login for this contact'); return false;}
 		if (document.form1.sub_password.value == ''){alert('Please enter a password for this contact'); return false;}
 		if (document.form1.sub_access.value == 'Disabled'){var checkdisable = confirm('Are you sure you want to disable this account');
 		if (checkdisable == true)
 		{
 		}
 		else
 		{
 			menu_focus(document.form1.sub_access,'Active');
 			return false;
 		}
 		return true;
 		}
 			
 	}
 	</script>";
 	bodyAndLoad("menu_focus(document.form1.company,\"$company\")");
 	ioiFont("The login you entered is already in use by another contact") if (param('error'));
 	print "<form name='form1' id='form1' action = '' onsubmit='return checkSubmit()'>
 			<input type='hidden' name='assigned_to' value='$assigned_to'>
 			<input type='hidden' name='old_user' value='$old_user'>
 			<input type='hidden' name='case_num' value='$case_num'>\n";
 	tableHead('50%');
 	print "<tr><td>Company</td><td>"; companyDropDown(); print "</td></tr>
 		   <tr><td>Name</td><td><input type='text' name='sub_name' value='$sub_name'></td></tr>
 		   <tr><td>Login</td><td><input type='text' name='sub_login' value='$sub_login'></td></tr>
 		   <tr><td>Password</td><td><input type='text' name='sub_password' value='ioi'></td></tr>
 		   <tr><td>Email</td><td><input type='text' name='sub_email' value='$sub_email'></td></tr>
 		   <tr><td>Phone</td><td><input type='text' name='sub_phone' value='$sub_phone'></td></tr>
 		   <tr><td>Cell Phone</td><td><input type='text' name='cell_phone' value='$sub_cell'></td></tr>
 		   <tr><td>Fax</td><td><input type='text' name='sub_fax' value='$sub_fax'></td></tr>
 		   <tr><td>Access</td><td><select name='sub_access'><option value='Active'>Active</option><option value='Disabled'>Disabled</option></select></td></tr>
		   <tr><td>Department</td><td><input type='text' name='sub_dept' value='$sub_dept'></td></tr>
		   <tr><td>Notes</td><td><textarea name='sub_notes' rows='10' cols='60'>$sub_notes</textarea></td></tr>
		   <tr><td colspan='2'><div align='center'><input type='submit' name='result' value='Create User'></div></td></tr>
		   </table></form>";
	end_html();
}
sub newUserRes()
{
	my $assigned_to = param('assigned_to');
	my $case_num = param('case_num');
	my $old_user = param('old_user');
	my $sub_name = param('sub_name');
	my $company = param('company');
	my $sub_login = param('sub_login');
	my $sub_email = lc(param('sub_email'));
	my $sub_password = param('sub_password');
	my $sub_email = param('sub_email');
	my $sub_phone = param('sub_phone');
	my $cell_phone = param('cell_phone');
	my $sub_fax = param('sub_fax');
	my $sub_access = param('sub_access');
	my $sub_dept = param('sub_dept');
	my $sub_notes = param('sub_notes');
	$sub_name = quoteValues($sub_name);
	$sub_notes = quoteValues($sub_notes);
	$sub_dept = quoteValues($sub_dept);
	$sub_email = quoteValues($sub_email);
	if ($old_user eq "VENDOR_EMAIL")
	{
		$id_num = selectValues("select max(id_num) from users");
		$id_num++;
		$statement = "select sub_login,sub_e_mail from users where sub_login = '$sub_login'";
		($check_login,$check_email) = selectValues($statement);
		if ($check_login ne "" or $check_email ne "")
		{
			print $cgi->redirect("changeUser.cgi?company=$company&assigned_to=$assigned_to&old_user=$old_user&case_num=$case_num&submit=Create%20User&error=duplicate");
		}
		$statement = "Insert into users (id_num,sub_name,sub_login,sub_e_mail,sub_phone,cell_phone,sub_fax,sub_dept,sub_access,sub_notes,sub_password,sub_comp_link)
		values ($id_num,$sub_name,'$sub_login',$sub_email,'$sub_phone','$cell_phone','$sub_fax',$sub_dept,'$sub_access',$sub_notes,'$sub_password','$sub_comp_link')";
		insert($statement);
		$statement = "UPDATE problem SET submitted_by = '$sub_login' where case_num = '$case_num'";
		insert($statement);
	}
	else
	{
		insert("update users set sub_name=$sub_name,sub_e_mail=$sub_email,sub_phone='$sub_phone',sub_dept=$sub_dept,sub_notes = $sub_notes,
		cell_phone='$cell_phone',sub_fax='$sub_fax',sub_access = '$sub_access',sub_password = '$sub_password',sub_comp_link='$company' where sub_login = '$old_user'");
	}
	insert("UPDATE problem SET assigned_to = '$assigned_to',status='Pending IOI' where case_num = '$case_num'");
	print $cgi->header();
	headers();
	background();
	bodyAndLoad();
	ioiFont("$sub_name has been added to the database.<p>Ticket # $case_num has been assigned to $assigned_to");
	end_HTML;
}
sub newUserComp()
{
my $assigned_to = param('assigned_to');
my $case_num = param('case_num');
my $old_user = param('old_user');
print $cgi->header();
headers();
print "<script language=\"JavaScript\" type=\"text/JavaScript\">
function checkSubmit()
{
 if (document.form1.comp_name.value == \"\")
{
 alert(\"Company Name must be entered\");
return false;
}
else {
return true;
}
}
  </script>
  
  <body>
<strong>Submit Company </strong></div>
<form name=\"form1\" method=\"get\" id=\"form1\" action=\"companySubmit.cgi\" onSubmit=\"return checkSubmit()\">
<input type=\"hidden\" name=\"case_num\" value=\"$case_num\">
<input type=\"hidden\" name=\"assigned_to\" value=\"$assigned_to\">
<input type=\"hidden\" name=\"old_user\" value=\"old_user\">
  <div align=\"center\">
    <table width=\"568\" height=\"513\" border=\"1\" bgcolor=\"#909090\">
      <tr>
        <th scope=\"row\">Company Name </th>
        <td><input name=\"comp_name\" type=\"text\" id=\"comp_name\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Phone Number </th>
        <td><input name=\"comp_phone\" type=\"text\" id=\"comp_phone\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Fax Number </th>
        <td><input name=\"comp_fax\" type=\"text\" id=\"comp_fax\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company WWW Address </th>
        <td><input name=\"comp_www\" type=\"text\" id=\"comp_www\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Billing Address </th>
        <td><input name=\"comp_bill_address\" type=\"text\" id=\"comp_bill_address\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Billing City </th>
        <td><input name=\"comp_bill_city\" type=\"text\" id=\"comp_bill_city\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Billing State </th>
        <td><input name=\"comp_bill_state\" type=\"text\" id=\"comp_bill_state\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Billing Zip </th>
        <td><input name=\"comp_bill_zip\" type=\"text\" id=\"comp_bill_zip\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Billing Country </th>
        <td><input name=\"comp_bill_country\" type=\"text\" id=\"comp_bill_country\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Shipping Address </th>
        <td><input name=\"comp_ship_address\" type=\"text\" id=\"comp_ship_address\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Shipping City </th>
        <td><input name=\"comp_ship_city\" type=\"text\" id=\"comp_ship_city\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Shipping State </th>
        <td><input name=\"comp_ship_state\" type=\"text\" id=\"comp_ship_state\"></td>
      </tr>
      <tr>
        <th scope=\"row\">Company Shipping Zip </th>
        <td><input name=\"comp_ship_zip\" type=\"text\" id=\"comp_ship_zip\"></td>
      </tr>
    </table>  
    <input type=\"submit\" name=\"Submit\" value=\"Submit\">
    <input type=\"reset\" name=\"Reset\" value=\"Reset\">
</div>
</form>";
end_HTML();
}
