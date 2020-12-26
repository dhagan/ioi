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
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
$loginString = "?sub_e_mail=$username&sub_email=$password&checkLogin=true";
($sub_e_mail, $sub_name, $sub_comp_link) = validateUser( 'support@iointegration.com', 'ioi101');
if ($sub_e_mail) {
   #print ($sub_e_mail, $sub_name, $sub_comp_link);
   print $cgi->redirect("helpdesk.cgi$loginString&redirect=$page");
} else {
print $cgi->header();
print "
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">
<title>IOI Dashboard</title>
</head>

<body>
Please login!
</body>
</html>
";
}
