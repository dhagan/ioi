#!/usr/bin/perl

################################################################################
#
#       File Name: staffappend.cgi
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
#staffAppend
use CGI;
use DBI;
$cgi = new CGI;
my $dbh = getDBConnection();
$dbh-> {'LongReadLen'} = 1000000; 
$case_num = $cgi->param('case_num');
$submitted_by = $cgi->param('submitted_by');
$inputBy = $cgi->param('inputBy');
$short_desc = $cgi->param('short_desc');
$sth = $dbh->prepare("SELECT sub_name,sub_phone,sub_comp_link FROM users WHERE sub_login = '$submitted_by'");
$sth->execute();
($sub_name,$sub_phone,$sub_comp_link) = $sth->fetchrow_array();
$sth = $dbh->prepare("SELECT comp_name FROM company WHERE comp_case_num = '$sub_comp_link'");
$sth->execute();
$comp_name = $sth->fetchrow_array();
print $cgi->header();
print $cgi->start_html();

print "<style type='text/css'>
<!--
body {
	background-color: #C0C0C0;
	
}
.style1 {color: #FF9900}
-->
</style>";
print "<div align='center'>
  <p class='style1'>Append to ticket $case_num</p>
  <form name='form1' action='staffAppendRes.cgi' method='get'>
  <input type='hidden' name='case_num' value='$case_num'>
  <table width='90%' border='1' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#FF9900'>
    <tr>
      <th width='50%' scope='row'>Customer</th>
      <td width='50%'>$sub_name</td><input type='hidden' name='customer' value='$sub_name'>
    </tr>
    <tr>
      <th scope='row'>Company</th>
      <td>$comp_name</td><input type = 'hidden' name='company' value='$comp_name'>
    </tr>
    <tr>
      <th scope='row'>Phone</th><input type='hidden' name='phone' value='$sub_phone'>
      <td>$sub_phone</td>
    </tr>
    <tr>
      <th scope='row'>Short Description </th>
      <td>$short_desc</td>
    </tr>
    <tr>
      <th scope='row' colspan='2'>Problem</th>
    </tr>
    <tr>
      <th scope='row' colspan='2'><textarea name='problem' cols='100' rows='8'></textarea></th>
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
  <input type='submit' name='Submit' value='Submit'>
  </form>
  <p>
     
  </p>
</div>
</body>
</html>";