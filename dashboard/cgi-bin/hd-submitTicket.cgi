#!/usr/bin/perl

################################################################################
#
#       File Name: techSubmit.cgi
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
#techSubmit
use DBI;
use CGI;
my $dbh = getDBConnection();
$cgi = new CGI;
$sub_login = $cgi->param('customer');
### DJH $user = $cgi->param('user');
$user = getRemoteUser();

print $cgi->header();
print "<html><head><title>Ticket Submit</title>
<meta http-equiv=\"Content-Type\" content=\"text/html;charset=iso-8859-1\">
<script language ='javascript'>
function setup()
{
	menu_focus(document.form1.assigned_to,'$user');
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
function formOnClick(thisAction)
{
	if (thisAction == \"vendor\")
	{
		document.form1.email_action.value = 'Email Vendor';
	}
	if (thisAction == \"client\")
	{
		document.form1.email_action.value = 'Email Client';
	}
	if (thisAction == \"none\")
	{
		document.form1.email_action.value= 'Submit';
	}
}
function checkSubmit()
{
	

	if (document.form1.assigned_to.value != '$user')
	{
		var checkAssign = confirm('Are you sure you want to assign this to someone other than yourself ($user)');
		if (checkAssign == true)
		{
		}
		else
		{
			menu_focus(document.form1.assigned_to,'$user');
			return false;
		}
	}
	
	if (document.form1.subject.value == '')
	{
		alert('Please enter a short description for this ticket');
		return false;
	}
		
	if (document.form1.problem.value == '')
	{
		alert('Please enter a problem for this ticekt');
		return false;
	}
	if (document.form1.time_spent.value == 0)
	{
		alert('Time Spent is an invalid value');
		return false;
	}

	if (document.form1.time_spent.value >= 1000)
	{	
				
	var checkOver = confirm('This time spent value is too high, if this was meant to be the vendor ticket number click yes');
	if (checkOver == true)
	{
	document.form1.xinet_ticket_num.value = document.form1.time_spent.value;
	}
	document.form1.time_spent.value = '';
	return false;
	}
	if (document.form1.product.value == '')
	{
		alert('Please select a product for this ticket');
		return false;
	}
				

}


</script></head><body onLoad='setup()'>";
print "<style type='text/css'>
<!--
body {
	background-color: #C0C0C0;
}

-->
</style>";
$sth = $dbh->prepare("select sub_phone,sub_e_mail,sub_name,sub_comp_link from users where sub_login = '$sub_login'");
$sth->execute();
($phone,$email,$name,$comp_case_num) = $sth->fetchrow_array();
$sth = $dbh->prepare("select comp_bill_address, comp_bill_city,comp_bill_state,comp_bill_zip from company where comp_case_num = '$comp_case_num'");
$sth->execute();
($comp_bill_address,$comp_bill_city,$comp_bill_state,$comp_bill_zip) = $sth->fetchrow_array();

print "<FORM ACTION=\"email2.cgi\" METHOD=\"POST\" ENCTYPE=\"multipart/form-data\" name=\"form1\" onsubmit='return checkSubmit()'>

<input type='hidden' name='user' value='$user'>
<input type='hidden' name='newticket' value='true'>
<input type='hidden' name='email_action'>
<input type='hidden' name='submitted_by' value='$sub_login'>
<input type='hidden' name='comp_case_num' value='$comp_case_num'>
<div align=\"center\">
  <p class=\"style1\"><font color='#808080' size='6mm'>Submit Ticket for $name</font></p>
  <table width=\"90%\"  border=\"1\" cellpadding=\"0\" cellspacing=\"0\" bordercolor=\"#C0C0C0\" bgcolor=\"#B0B0B0\">
    <tr>
      <td colspan=\"4\" bgcolor=\"#909090\" class=\"style1\"><div align=\"center\" class=\"style2\">Email: <strong>$email</strong> Phone: <strong>$phone</strong> Cell: <strong>$cell </strong></div></td>
    </tr>
    <tr bgcolor=\"#909090\">
      <td colspan=\"4\"><div align=\"center\" class=\"style2\">Bill Address: $comp_bill_address $comp_bill_city $comp_bill_state $comp_bill_zip </div></td>
    </tr>
      <tr bgcolor=\"#909090\">
      <td colspan=\"4\"><div align=\"center\" class=\"style2\">Serial #'s: ";
      $sth = $dbh->prepare("select prod_name,prod_part_num from product where prod_comp_link = '$comp_case_num'");
      $sth->execute();
      while(($prod_name,$prod_part_num) = $sth->fetchrow_array())
     { 
     print "$prod_name: <b>$prod_part_num</b> &nbsp;" if ($prod_part_num ne "");
     } 
      
      print"</div></td>
    </tr>
    <tr>
      <td><span class=\"style3\">Product: <select name=\"product\" id=\"product\">
        <option value=\"\"></option>";
        $sth = $dbh->prepare("select prod_name,prod_case_num from product where prod_comp_link = '$comp_case_num'");
        $sth->execute();
        while (($prod_name,$prod_case_num) = $sth->fetchrow_array())
        {
        	print "<option value='$prod_case_num'>$prod_name</option>";
        }
  print"  
	  </select></span></td>
      <td>Priority: 
        <select name=\"priority\" id=\"priority\">
                  <option value=\"Critical\">Critical</option>
          <option value=\"High\">High</option>
          <option value=\"Medium\">Medium</option>
          <option value=\"Low\">Low</option>
          </select></td>
      <td>Assign To: 
        <select name=\"assigned_to\" id=\"assigned_to\">";
        $sth = $dbh->prepare("select sa_login,sa_name from staff where sa_dept = 'IT' and sa_access = 'Active'");
        $sth->execute();
        while(($sa_login,$sa_name) = $sth->fetchrow_array())
        {
        	print "<option value='$sa_login'>$sa_name</option>";
        }
        print "<option value='nobody'>nobody</option>";
        print"
        
        </select></td>
      <td>Status: 
        <select name=\"status\" id=\"status\">
         <option value=\"Open\">Open</option>
          <option value=\"Assigned\">Assigned</option>
          <option value=\"Pending Vendor\">Pending Vendor</option>
          <option value=\"Pending Client\">Pending Client</option>
          <option value=\"Pending IOI\">Pending IOI</option>
          <option value=\"Awaiting Feature Request\">Awaiting Feature Request</option>
          <option value=\"Awaiting Bug Fix\">Awaiting Bug Fix</option>
          <option value=\"Closed\">Closed</option>
        </select></td>
    </tr>
    <tr>
      <td>Time Spent: 
      <input name=\"time_spent\" type=\"text\" size=\"5\"></td><td>Vendor Ticket: <input type='text' name='xinet_ticket_num' value=''></td>
      <td>Subject:</td><td colspan=\"1\"><input name=\"subject\" type=\"text\" size=\"75\"></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"center\">Problem: </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"center\">
        <textarea name=\"problem\" cols=\"95\" rows=\"15\"></textarea>
      </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"center\">Attachment 1 
        <input type=\"FILE\" name=\"attachment1\">
      </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"center\">Attachment 2 
        <input type=\"file\" name=\"attachment2\">
      </div></td>
    </tr>
    <tr>
      <td colspan=\"4\"><div align=\"center\">Attachment 3 
        <input type=\"file\" name=\"attachment3\">
      </div></td>
    </tr>

  </table>
  <p class=\"style1\">
<input type='submit' name='button' value='Email Vendor' onClick='formOnClick(\"vendor\")'>
	  		<input type='submit' name='button' value='Email Client' onClick='formOnClick(\"client\")'>
	  		<input type='submit' name='button' value='No Email' onClick='formOnClick(\"none\")'>
    <input type=\"reset\" name=\"Reset\" value=\"Reset\">
  </p>
</div>
</form>
</body>
</html>";
