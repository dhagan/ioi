#!/usr/bin/perl

################################################################################
#
#       File Name: login.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 20010IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#
################################################################################

use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
($sub_e_mail, $sub_name, $sub_comp_link) = &getUserSession();
if ($sub_e_mail && $sub_name && $sub_comp_link) {
   $loginString = "?sub_e_mail=$sub_e_mail&sub_name=$sub_name&sub_comp_link=$sub_comp_link";
   $url = "helpdesk.cgi$loginString&redirect=$page";
   print $cgi->redirect(-uri => $url);
   exit;
} 

$sub_e_mail=$cgi->param('username');
$sub_password=$cgi->param('password');
$invalidate=$cgi->url_param('invalidate');
($sub_e_mail, $sub_name, $sub_comp_link) = &validateUser( $sub_e_mail, $sub_password);
if ($sub_e_mail && $sub_name && $sub_comp_link) {
   setUserSession($sub_e_mail, $sub_name, $sub_com_link);
   $loginString = "?sub_e_mail=$sub_e_mail&sub_name=$sub_name&sub_comp_link=$sub_comp_link";
   $url = "helpdesk.cgi$loginString&redirect=$page";
   print $cgi->redirect(-uri => $url);
   exit;
} elsif ($invalidate)
{
   print $cgi->header();
   print "Unable to authenticate, please try again.";
   exit;
} else 
{
   $session = CGI::Session->new($cgi) or die CGI->Session->errstr;
   print $session->header();
   print $cgi->param;
   print "
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">
<meta name=\"viewport\" content=\"width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;\"/>  
<title>IOI Tickets</title>
<link href=\"status.css\" rel=\"stylesheet\" type=\"text/css\">
</head>
<body>
<form action=\"hd-login.cgi?invalidate=1\" method=\"post\" name=\"login\" id=\"login\">
    <table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" id=\"status\" summary=\"Active tickets.\">
        <caption align=\"top\"  class=\"login\">
        Welcome to the IOI Tickets
        </caption>
        <tr>
            <td class=\"login\">Username: </td>
            <td class=\"login\"><input name=\"username\" type=\"text\" id=\"username\" size=\"20\" maxlength=\"156\"  value=\"\"></td>
        </tr>
        <tr>
            <td class=\"login\">Password: </td>
            <td class=\"login\"><input name=\"password\" type=\"password\" id=\"password\" size=\"20\" maxlength=\"156\"></td>
        </tr>
        <tr>
            <td  class=\"login\" colspan=\"2\"><input type=\"submit\" name=\"Submit\" value=\"Submit\"></td>
        </tr>
        <tr>
            <td colspan=\"2\" class=\"copyright\"> Copyright &copy; 2021 IO Integration, Inc. All rights reserved.</td>
        </tr>
    </table>
</form>
</body>
</html>

";
   exit;
}

