#!/usr/bin/perl

################################################################################
#
#       File Name: status.cgi
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

<frameset rows=\"65,*\" frameborder=\"NO\" border=\"0\" framespacing=\"0\">
  <frame src=\"/cgi-bin/navbar.cgi\" name=\"topFrame\" scrolling=\"NO\" noresize >
  <frame src=\"/status/index.php?username=$user&password=fred\" name=\"mainFrame\">
</frameset>
<noframes><body>
</body></noframes>
</html>
";