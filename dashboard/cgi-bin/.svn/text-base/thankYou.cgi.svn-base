#!/usr/bin/perl

################################################################################
#
#       File Name: thankYou.cgi
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
$cgi = new CGI;
print $cgi->header();
$user = $ENV{"REMOTE_USER"};
$user =~ s/IOINTEGRATION\\//g;
print "
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">
<title>IOI Dashboard</title>
</head>

<body>
Thank you!
</body>
</html>
";
