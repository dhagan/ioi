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
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
$cgi = new CGI;
$session = CGI::Session->new($cgi) or die CGI->Session->errstr;
$session->delete();
$session->flush();
print $cgi->header();
print "
<html>
<head>
<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">
<title>IOI Dashboard</title>
</head>

<body>
Logout success!
</body>
</html>
";
