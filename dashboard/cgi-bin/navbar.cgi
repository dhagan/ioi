#!/usr/bin/perl

################################################################################
#
#       File Name: navbar.cgi
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
#       01/25/2007      B. Scarborough  Modifed image sources in some places to point to /images/ instead of images/
#       12/20/2007      B. Covington    Modified Login Table link
################################################################################

use CGI;
$cgi = new CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$user = $ENV{REMOTE_USER};
open(KEY,"< /Library/WebServer_SSL/key");
$key = <KEY>;
chomp($key);
close KEY;
$i = getQueryCount("select case_num from problem where assigned_to ='nobody'");
print $cgi->header();
print "

<html>
<head>";
autoRefresh();
print"
<title>navbar.gif</title>
<meta http-equiv=\"Content-Type\" content=\"text/html;\">
<!--Fireworks MX 2004 Dreamweaver MX 2004 target.  Created Sun Sep 25 18:23:16 GMT-0700 ( ) 2005-->
<script language=\"JavaScript\">
<!--
function MM_findObj(n, d) { //v4.01
  var p,i,x;  if(!d) d=document; if((p=n.indexOf(\"?\"))>0&&parent.frames.length) {
    d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
  if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
  for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
  if(!x && d.getElementById) x=d.getElementById(n); return x;
}
function MM_nbGroup(event, grpName) { //v6.0
var i,img,nbArr,args=MM_nbGroup.arguments;
  if (event == \"init\" && args.length > 2) {
    if ((img = MM_findObj(args[2])) != null && !img.MM_init) {
      img.MM_init = true; img.MM_up = args[3]; img.MM_dn = img.src;
      if ((nbArr = document[grpName]) == null) nbArr = document[grpName] = new Array();
      nbArr[nbArr.length] = img;
      for (i=4; i < args.length-1; i+=2) if ((img = MM_findObj(args[i])) != null) {
        if (!img.MM_up) img.MM_up = img.src;
        img.src = img.MM_dn = args[i+1];
        nbArr[nbArr.length] = img;
    } }
  } else if (event == \"over\") {
    document.MM_nbOver = nbArr = new Array();
    for (i=1; i < args.length-1; i+=3) if ((img = MM_findObj(args[i])) != null) {
      if (!img.MM_up) img.MM_up = img.src;
      img.src = (img.MM_dn && args[i+2]) ? args[i+2] : ((args[i+1])?args[i+1] : img.MM_up);
      nbArr[nbArr.length] = img;
    }
  } else if (event == \"out\" ) {
    for (i=0; i < document.MM_nbOver.length; i++) { img = document.MM_nbOver[i]; img.src = (img.MM_dn) ? img.MM_dn : img.MM_up; }
  } else if (event == \"down\") {
    nbArr = document[grpName];
    if (nbArr) for (i=0; i < nbArr.length; i++) { img=nbArr[i]; img.src = img.MM_up; img.MM_dn = 0; }
    document[grpName] = nbArr = new Array();
    for (i=2; i < args.length-1; i+=2) if ((img = MM_findObj(args[i])) != null) {
      if (!img.MM_up) img.MM_up = img.src;
      img.src = img.MM_dn = (args[i+1])? args[i+1] : img.MM_up;
      nbArr[nbArr.length] = img;
  } }
}

function MM_preloadImages() { //v3.0
 var d=document; if(d.images){ if(!d.MM_p) d.MM_p=new Array();
   var i,j=d.MM_p.length,a=MM_preloadImages.arguments; for(i=0; i<a.length; i++)
   if (a[i].indexOf(\"#\")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}

//-->
</script>
</head>
<body bgcolor=\"#C0C0C0\" onLoad=\"MM_preloadImages('/images/helpdesk_f2.gif','/images/helpdesk_f4.gif','/images/helpdesk_f3.gif','/images/status_page_f2.gif','/images/status_page_f4.gif','/images/status_page_f3.gif','/images/status_page.gif','/images/management_f2.gif','/images/management_f4.gif','/images/management_f3.gif','/images/contacts_f2.gif','/images/contacts_f4.gif','/images/contacts_f3.gif','/images/utilities_f2.gif','/images/utilities_f4.gif','/images/utilities_f3.gif');\">
<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"789\" align='center'>
<!-- fwtable fwsrc=\"navbar.png\" fwbase=\"navbar.gif\" fwstyle=\"Dreamweaver\" fwdocid = \"127280570\" fwnested=\"0\" -->
  <tr>
   <td><img src=\"/images/spacer.gif\" width=\"156\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"156\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"156\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"156\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"156\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"1\" height=\"1\" border=\"0\" alt=\"\"></td>
   <td><img src=\"/images/spacer.gif\" width=\"1\" height=\"1\" border=\"0\" alt=\"\"></td>
  </tr>

  <tr>
   <td><a href=\"/subframe.htm\" target=\"mainFrame\" onMouseOut=\"MM_nbGroup('out');\" onMouseOver=\"MM_nbGroup('over','helpdesk','/images/helpdesk_f2.gif','/images/helpdesk_f4.gif',1);\" onClick=\"MM_nbGroup('down','navbar1','helpdesk','/images/helpdesk_f3.gif',1);\"><img name=\"helpdesk\" src=\"/images/helpdesk.gif\" width=\"156\" height=\"40\" border=\"0\" alt=\"\"></a></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"40\" border=\"0\" alt=\"\"></td>
   <td><a href=\"/status/index.php\" target=\"mainFrame\" onMouseOut=\"MM_nbGroup('out');\" onMouseOver=\"MM_nbGroup('over','status_page','/images/status_page_f2.gif','/images/status_page_f4.gif',1);\" onClick=\"MM_nbGroup('down','navbar1','status_page','/images/status_page_f3.gif',1);top.mainFrame.location.href='/status/index.php?username=$user&password=fred';return false;\"><img name=\"status_page\" src=\"/images/status_page_f3.gif\" width=\"156\" height=\"40\" border=\"0\" alt=\"\"onLoad=\"MM_nbGroup('init','navbar1', 'status_page','/images/status_page.gif',1)\"></a></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"40\" border=\"0\" alt=\"\"></td>
   <td><a href=\"/cgi-bin/management.cgi\" target=\"mainFrame\" onMouseOut=\"MM_nbGroup('out');\" onMouseOver=\"MM_nbGroup('over','management','/images/management_f2.gif','/images/management_f4.gif',1);\" onClick=\"MM_nbGroup('down','navbar1','management','/images/management_f3.gif',1);\"><img name=\"management\" src=\"/images/management.gif\" width=\"156\" height=\"40\" border=\"0\" alt=\"\"></a></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"40\" border=\"0\" alt=\"\"></td>
   <td><a href=\"/subFrame2.htm\" target=\"mainFrame\" onMouseOut=\"MM_nbGroup('out');\" onMouseOver=\"MM_nbGroup('over','contacts','/images/contacts_f2.gif','/images/contacts_f4.gif',1);\" onClick=\"MM_nbGroup('down','navbar1','contacts','/images/contacts_f3.gif',1);\"><img name=\"contacts\" src=\"/images/contacts.gif\" width=\"156\" height=\"40\" border=\"0\" alt=\"\"></a></td>
   <td><img src=\"/images/spacer.gif\" width=\"2\" height=\"40\" border=\"0\" alt=\"\"></td>
   <td><a href=\"/reportsFrame.htm\" target=\"mainFrame\" onMouseOut=\"MM_nbGroup('out');\" onMouseOver=\"MM_nbGroup('over','utilities','/images/utilities_f2.gif','/images/utilities_f4.gif',1);\" onClick=\"MM_nbGroup('down','navbar1','utilities','/images/utilities_f3.gif',1);\"><img name=\"utilities\" src=\"/images/utilities.gif\" width=\"156\" height=\"40\" border=\"0\" alt=\"\"></a></td>
   <td><img src=\"/images/spacer.gif\" width=\"1\" height=\"40\" border=\"0\" alt=\"\"></td>
   <td><a href=\"/cgi-bin/newsblog.cgi\" target=\"mainFrame\" onMouseOut=\"MM_nbGroup('out');\" onMouseOver=\"MM_nbGroup('over','newsblog','/images/newsblog_f2.gif','/images/newsblog_f2.gif',1);\" onClick=\"MM_nbGroup('down','navbar1','newsblog','/images/newsblog_f3.gif',1);\"><img name=\"newsblog\" src=\"/images/newsblog.gif\" width=\"156\" height=\"40\" border=\"0\" alt=\"\"></a></td>
   <td><img src=\"/images/spacer.gif\" width=\"1\" height=\"40\" border=\"0\" alt=\"\"></td>
   <td><a href = 'https://dashboard.iointegration.com/cgi-binssl/loginSearch.pl?key=$key&loginSearch=yes' target='_blank'>Login Table</a></td>
  </tr>
  <tr "; print "bgcolor='#B0B0B0'" if ($i>0); print" >
     <td height='0' colspan='11'"; print" bordercolor='#B0B0B0'" if ($i>0); print" >"; 
     print "<div align=\"center\"><a href=\"filterTickets.cgi\" class=\"style1\" target='mainFrame'>There is $i unassigned ticket </a></div>" if ($i ==1);
     print "<div align=\"center\"><a href=\"filterTickets.cgi\" class=\"style1\" target='mainFrame'>There are $i unassigned tickets </a></div>" if ($i >1);
     print "</td>
  </tr>
</table>
</body>
</html>
";
