#!/usr/bin/perl -w

################################################################################
#
#       File Name: ioistyle.cgi
#
#       Purpose: This file is used for styling the web pages and is used by
#                files in the dashboard and support webistes, as well as in
#                ticketReminder.pl
#
#       Copyright © 2005 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       ??/??/????      M. Smith        Created this file
#       01/25/2007      B. Scarborough  Modified headers() to add orange links
#       03/13/2007      B. Scarborough  Modified headers() to display title
################################################################################

# Function: headers
# Purpose: Displays HTML header information
# Inputs: title(optional)
# Returns: None

sub headers()
{
	my $title = $_[0] if ( $_[0] );
	print "
<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en-US\" xml:lang=\"en-US\"><head><title>$title</title>
<style type='text/css'>
a.orange:link {color:orange}
a.orange:visited {color:orange}
a.orange:hover {color:white}
a.orange:active {color:orange}
</style>";
}
sub smallFont()
{
		print "<style type='text/css'>
	<!--
	body,td,th {
		font-size: 12 px;
	}
	-->
	</style>";
}
sub autoRefresh()
{
	$time = $_[0];
	$time = 200000 if ($time eq "");
	print "<script type=text/javascript>
// The time out value is set to be 10,000 milli-seconds (or 10 seconds)
setTimeout(' document.location=document.location' ,$time);
</script>";
}	
sub ioiFont()
{
	my $phrase = $_[0] if ($_[0]);
	### DJH 9/16/2010
	###print "<center><font color='#000000'>$phrase</font></center>";
	print "<font color='#000000'>$phrase</font>";
}
sub background()
{

	print"<style type='text/css'>
	<!--
	body {
	background-color: #C0C0C0;
	}
	-->
	</style>";
	#return 1;
}
sub menu_focus()
{
print"<script language ='javascript'>	
function menu_focus(el,val)
{
        var     j;
        el_length=el.length;
        for(j=0;j<el_length;j++){
                if(el.options[j].value==val){
                        el.selectedIndex=j;
                }
         }
}
</script>
"
}
sub tableHead()
{
	my $width = $_[0] if ($_[0]);
	my $options = $_[1];
	print "<table width='$width'  border='1' align='center' cellpadding='5' cellspacing='0' bordercolor='#C0C0C0' bgcolor='#909090' $options>";
}
sub bodyAndLoad()
{
	my $options = $_[0] if ($_[0]);
	print "</head><body onLoad = '$options'>";
	return 1;
}
sub end_HTML()
{
	print "</body></html>";
	return 1;
}
sub statusDropDown()
{
	print "<select name='status'>
	<option value=''></option>
	<option value='Open'>Open</option>
	<option value='Pending IOI'>Pending IOI</option>
	<option value='Pending Client'>Pending Client</option>
	<option value='Pending Vendor'>Pending Vendor</option>
	<option value='Awaiting Bug Fix'>Awaiting Bug Fix</option>
	<option value='Awaiting Feature Request'>Awaiting Feature Request</option>
	<option value='Closed'>Closed</option>
	</select>";
}
sub priorityDropDown()
{
    my $priority = $_[0] if ($_[0]);
    my @priorities = ("Critical", "High", "Medium", "Low");

	print "<select name='priority'>
	<option value=''></option>";
	
	foreach (@priorities) {
        print "
        <option value='$_'";
        print " selected" if ($_ eq $priority);
        print ">$_</option>";
	}
	print "
	</select>";
}
sub dateDropDown() #for creating a date drop down, takes arguments (name of day menu,name of month menu,name of year menu)
			#will then make the menu name dayARGUMENT monthARGUMENT yearARGUMENT otherwise names it just day,month,year.
{
	my $day_name = $_[0] if ($_[0]);
	my $month_name = $_[1] if ($_[1]);
	my $year_name = $_[2] if ($_[2]);
	print "<select name='month$month_name'><option value=''></option>";
  	   for (my $i = 1;$i<=12; $i++)
 	 {
  		print "<option value = '0$i'>$i</option>" if ($i < 10);
  		print "<option value ='$i'>$i</option>" if ($i >= 10);
  	 }
	print "</select><select name='day$day_name'><option value=''></option>";
  	for (my $i = 1; $i < 32; $i++)
 	 { 	
 	 	print "<option value ='$i'>$i</option>" if ($i >= 10);
 	 	print "<option value='0$i'>$i</option>" if ($i < 10);
  	 }
  	 print "</select><select name='year$year_name'><option value=''></option>";
  	  for (my $i = 2001;$i<= 2012; $i++)
  	  {
  	  	print "<option value = '$i'>$i</option>";
  	  }
  	  print "</select>";
}

# Function: loginScreen
# Purpose: Displays login screen for support.iointegration.com
# Inputs: None
# Returns: None

sub loginScreen()
{
	print "<meta http-equiv=\"pragma\" content=\"no-cache\"></meta> 
	<title>
		HelpDesk Expert for Customer Service
	</title>";
	print "<script language=\"javascript\" type=\"text/javascript\">
		if (self != top) {
   			 if (document.images)
      		  top.location.replace(window.location.href);
  		  else
  		     top.location.href = window.location.href;
		}
		</script>
<STYLE TYPE=\"text/css\" MEDIA=\"screen\">

	.clearthis {
		clear: both;
		font-size: 2px;
		float: none;
		color: #FFFFFF;
	}
	
	BODY{
	SCROLLBAR-ARROW-COLOR: '#ebecee';
	SCROLLBAR-TRACK-COLOR: '#BACFE4';
	SCROLLBAR-BASE-COLOR: '#BACFE4';
	SCROLLBAR-DARK-SHADOW-COLOR: '#002E5F';
	SCROLLBAR-LIGHT-SHADOW-COLOR: '#BACFE4';
	SCROLLBAR-HIGHLIGHT-COLOR: '#002E5F';
	SCROLLBAR-FACE-COLOR: '#002E5F';
	SCROLLBAR-SHADOW-COLOR: '#002E5F';
	SCROLLBAR-3DLIGHT-COLOR: '#BACFE4';
	font-face: Tahoma, Verdana, Arial, Helvetica;
	background-color: #909090;
	}
	
	A:link, A:visited, A:active, A:hover{
		color: '#002E5F';
		text-decoration: underline;
	}
	
	P {
		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	hr {
		width: 100%;
		color: '#C0C0C0';
	}
	
	.formfield {
 		BORDER-RIGHT: #C0C0C0 2px solid;
 		BORDER-TOP: #C0C0C0 2px solid;
 		FONT-SIZE: 8pt;
 		BORDER-LEFT: #C0C0C0 2px solid;
 		CURSOR: auto;
		COLOR: '#000000';
		BORDER-BOTTOM: #C0C0C0 2px solid;
 		FONT-FAMILY: Tahoma, Verdana, Arial, Helvetica;
	}
	
	.formtextarea {
 		BORDER-RIGHT: #C0C0C0 2px solid;
 		BORDER-TOP: #C0C0C0 2px solid;
 		FONT-SIZE: 8pt;
 		BORDER-LEFT: #C0C0C0 2px solid;
 		CURSOR: auto;
		COLOR: '#000000';
		BORDER-BOTTOM: #C0C0C0 2px solid;
 		FONT-FAMILY: Tahoma, Verdana, Arial, Helvetica;
	}
	
	.formselect {
 		BORDER-RIGHT: #C0C0C0 2px solid;
 		BORDER-TOP: #C0C0C0 2px solid;
 		FONT-SIZE: 8pt;
 		BORDER-LEFT: #C0C0C0 2px solid;
 		CURSOR: auto;
		COLOR: '#000000';
		BORDER-BOTTOM: #C0C0C0 2px solid;
 		FONT-FAMILY: Tahoma, Verdana, Arial, Helvetica;
	}
	
	.enforce_formfield {
 		background-color: '#BACFE4';
 		BORDER-RIGHT: #C0C0C0 2px solid;
 		BORDER-TOP: #C0C0C0 2px solid;
 		FONT-SIZE: 8pt;
 		BORDER-LEFT: #C0C0C0 2px solid;
 		CURSOR: auto;
		COLOR: '#000000';
		BORDER-BOTTOM: #C0C0C0 2px solid;
 		FONT-FAMILY: Tahoma, Verdana, Arial, Helvetica;
	}
	
	.enforce_formtextarea {
 		background-color: '#BACFE4';
 		BORDER-RIGHT: #C0C0C0 2px solid;
 		BORDER-TOP: #C0C0C0 2px solid;
 		FONT-SIZE: 8pt;
 		BORDER-LEFT: #C0C0C0 2px solid;
 		CURSOR: auto;
		COLOR: '#000000';
		BORDER-BOTTOM: #C0C0C0 2px solid;
 		FONT-FAMILY: Tahoma, Verdana, Arial, Helvetica;
	}
	
	.enforce_formselect {
 		background-color: '#BACFE4';
 		BORDER-RIGHT: #000000 1px solid;
 		BORDER-TOP: #000000 1px solid;
 		FONT-SIZE: 8pt;
 		BORDER-LEFT: #000000 1px solid;
 		CURSOR: auto;
		COLOR: '#000000';
		BORDER-BOTTOM: #000000 1px solid;
 		FONT-FAMILY: Tahoma, Verdana, Arial, Helvetica;
	}
	
	H2 {
 		color: #FFFFFF;
 		font-size: 8pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
 		text-decoration: none;
		margin-bottom: 0;
		padding-bottom: 0;
	}
	
	a.whitelink:link, a.whitelink:visited, a.whitelink:active, a.whitelink:hover {
 		text-decoration: underline;
 		color: '#ffffff';
 		font-size: 10pt;
		font: bold;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.graylink:link, a.graylink:visited, a.graylink:active, a.graylink:hover {
 		text-decoration: none;
 		color: '#555C5F';
 		font-size: 10pt;
		font: bold;
		font-variant: small-caps;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.inpagelinks:link, a.inpagelinks:visited, a.inpagelinks:active, a.inpagelinks:hover {
 		text-decoration: underline;
 		color: '#555C5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
	}
	
	a.faqlink:link, a.faqlink:visited, a.faqlink:active{
 		text-decoration: underline;
 		color: '#000000';
 		font-size: 10pt;
		font: bold;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.faqlink:hover {
 		text-decoration: underline;
 		color: '#002E5F';
 		font-size: 10pt;
		font: bold;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.printlink:link, a.printlink:visited, a.printlink:active{
 		text-decoration: none;
 		color: '#555C5F';
 		font-size: 8pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
	}
	
	a.printlink:hover {
 		text-decoration: underline;
 		color: '#555C5F';
 		font-size: 8pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
	}
	
	a.plusminuslink:link, a.plusminuslink:visited, a.plusminuslink:active, a.plusminuslink:hover {
 		text-decoration: none;
 		color: '#002E5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	.problemheader {
 		color: '#555C5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
		font: bold;
	}
	
	.calendarnumeven {
 		color: '#555C5F';
 		font-size: 8pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font: bold;
		border-right: #808080 1px solid;
 		border-bottom: #808080 1px solid;
		background-color: '#ffffff';
		padding: 5;
	}
	
	.calendarnumodd {
 		color: '#555C5F';
 		font-size: 8pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font: bold;
		border-right: #808080 1px solid;
 		border-bottom: #808080 1px solid;
		background-color: '#ebecee';
		padding: 5;
	}
	
	.samelinetitle {
 		color: '#555C5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font: bold;
	}
	
	p.tabledivider {
 		color: '#555C5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
		font: bold;
	}
	
	p.tabledividerheader {
 		color: '#ffffff';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
		font: bold;
	}
	
	.tabledividerheaderfont {
 		color: '#ffffff';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
		font: bold;
	}
	
	p.tipmessages {
 		color: '#808080';
 		font-size: 8pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font: bold;
	}
	
	p.tableheadertext {
 		color: '#ffffff';
 		font-size: 12pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font: bold;
		letter-spacing: 1px;
	}
	
	p.attachmentheader {
 		color: '#555C5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
		font: bold;
	}
	
	p.pageheader {
 		color: '#000000';
 		font-size: 14pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font: bold;
		letter-spacing: 1px;
	}
	
	p.footerclass {
 		color: '#555C5F';
 		font-size: 8pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	p.inpagelinks {
 		color: '#555C5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font-variant: small-caps;
		font: bold;
	}
	
	a.pagelink:link, a.pagelink:visited, a.pagelink:active{
		padding: 8px 10px 8px 10px;
		margin: 0px 0px  0px 0px;
		border-right: 1px solid '#808080';
		border-left: 1px solid '#808080';
		border-top: 1px solid '#808080';
 		background-color: '#ebecee';
		text-align: center;
		line-height: 19px;
 		text-decoration: none;
 		color: '#555C5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.pagelink:hover{
		padding: 8px 10px 8px 10px;
		margin: 0px 0px  0px 0px;
		border-right: 1px solid '#808080';
		border-left: 1px solid '#808080';
		border-top: 1px solid '#808080';
		text-align: center;
		line-height: 19px;
 		text-decoration: none;
 		background-color: '#ffffff';
 		color: '#002E5F';
 		font-size: 11pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.activepagelink:link, a.activepagelink:visited{
		padding: 8px 10px 8px 10px;
		margin: 0px 0px  0px 0px;
		border-right: 1px solid '#808080';
		border-left: 1px solid '#808080';
		border-top: 1px solid '#808080';
 		background-color: '#BACFE4';
		text-align: center;
		line-height: 19px;
 		text-decoration: none;
 		color: '#000000';
 		font-size: 11pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.activepagelink:hover{
		padding: 8px 10px 8px 10px;
		margin: 0px 0px  0px 0px;
		border-right: 1px solid '#808080';
		border-left: 1px solid '#808080';
		border-top: 1px solid '#808080';
		text-align: center;
		line-height: 19px;
 		text-decoration: none;
 		background-color: '#ffffff';
 		color: '#002E5F';
 		font-size: 11pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	td.headerrow{
		padding: 4px 10px 4px 10px;
		margin: 0px 0px  0px 0px;
		border-right: 1px solid '#808080';
		border-left: 1px solid '#808080';
		border-top: 1px solid '#808080';
		text-align: center;
		line-height: 19px;
 		text-decoration: none;
 		background-color: '#ffffff';
 		color: '#002E5F';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
	}
	
	a.helpbutton {
 		cursor: help;
	}
	
	p.resultheader {
 		color: '#000000';
 		font-size: 12pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		font: bold;
		letter-spacing: 1px;
	}
	
	p.resultsmallheader {
 		color: '#000000';
 		font-size: 10pt;
 		font-family: Tahoma, Verdana, Arial, Helvetica;
		letter-spacing: 1px;
	}
	
body,td,th {
	color: #FFFFFF;
}
a:link {
	color: #CCCCCC;
}
a:visited {
	color: #CCCCCC;
}
a:hover {
	color: #CCCCCC;
}
a:active {
	color: #CCCCCC;
}
.style3 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px; font-weight: bold; }
</STYLE>

<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
<script language=\"JavaScript\" type=\"text/JavaScript\">
<!--



function MM_preload/images() { //v3.0
  var d=document; if(d./images){ if(!d.MM_p) d.MM_p=new Array();
    var i,j=d.MM_p.length,a=MM_preload/images.arguments; for(i=0; i<a.length; i++)
    if (a[i].indexOf(\"#\")!=0){ d.MM_p[j]=new Image; d.MM_p[j++].src=a[i];}}
}
//-->
</script>
</head>

<body>


<center>
			<table width=\"519\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\" align='center'>
              <tr>
                <td colspan=\"3\"><img src=\"/images/login_top.gif\" width=\"519\" height=\"177\"></td>
              </tr>
              <tr>
                <td width=\"46\"><img src=\"/images/login_left.gif\" width=\"46\" height=\"142\"></td>
                <td width=\"425\" bgcolor=\"#FF9933\"><br>                  <table width=\"400\" border=\"0\" align=\"center\" cellpadding=\"4\" cellspacing=\"0\">
                  <tr>
                  <form name=\"form1\" method=\"post\" action=\"/cgi-bin/customer.cgi\">";
                  print "<input type='hidden' name='redirect' value='". param('redirect') . "'>" if param('redirect');
                  print "
                  <input type='hidden' name='checkLogin' value='yes'>
                    <td width=\"156\"><div align=\"right\"><span class=\"style3\">user name</span></div></td>
                    <td width=\"228\"><div align=\"left\"><input name=\"username\" type=\"text\" size=\"20\">
                    </div></td>
                  </tr>
                  <tr>
                    <td><div align=\"right\"><span class=\"style3\">password</span></div></td>
                    <td>
                      <div align=\"left\">
                        <input name=\"password\" type=\"password\" size=\"20\">
                    </div></td>
                  </tr>
                  <tr>
                    <td colspan=\"2\">
                      
                      <div align=\"center\"> <br>
                        <input type=\"submit\" name=\"Submit\" value=\"login\">
                      </div></form></td>
                  </tr>
                </table>                </td>
                <td width=\"48\"><img src=\"/images/login_right.gif\" width=\"48\" height=\"142\"></td>
              </tr>
              <tr>
                <td colspan=\"3\"><img src=\"/images/login_btm.gif\" width=\"519\" height=\"77\"></td>
              </tr>
  </table>
			<p><br>
			<div align='center'>
		    <font face=\"Tahoma, Verdana, Arial, Helvetica\" size=\"2\">If you have any questions regarding this tool please email </font> <font face=\"Tahoma, Verdana, Arial, Helvetica\" size=\"2\"> <strong> <a href=\"mailto:support\@iointegration.com\"> support\@iointegration.com</a></strong></font></p>
  <blockquote>
   	 <img src=\"/images/IO_logo_btm.gif\" width=\"276\" height=\"98\"></blockquote></center>
</center>
<p></body>
</html>";
}
sub stateDropDown()
{
	print "<select name=\"state\">
		<option value=\"\"></option>
        <option value=\"AL\">AL</option>
        <option value=\"AK\">AK</option>
        <option value=\"AZ\">AZ</option>
        <option value=\"AR\">AR</option>
        <option value=\"CA\">CA</option>
        <option value=\"CO\">CO</option>
        <option value=\"CT\">CT</option>
        <option value=\"DE\">DE</option>
        <option value=\"DC\">DC</option>
        <option value=\"FL\">FL</option>
        <option value=\"GA\">GA</option>
        <option value=\"HI\">HI</option>
        <option value=\"ID\">ID</option>
        <option value=\"IL\">IL</option>
        <option value=\"IN\">IN</option>
        <option value=\"IA\">IA</option>
        <option value=\"KS\">KS</option>
        <option value=\"KY\">KY</option>
        <option value=\"LA\">LA</option>
        <option value=\"ME\">ME</option>
        <option value=\"MD\">MD</option>
        <option value=\"MA\">MA</option>
        <option value=\"MI\">MI</option>
        <option value=\"MN\">MN</option>
        <option value=\"MS\">MS</option>
        <option value=\"MO\">MO</option>
        <option value=\"MT\">MT</option>
        <option value=\"NE\">NE</option>
        <option value=\"NV\">NV</option>
        <option value=\"NH\">NH</option>
        <option value=\"NJ\">NJ</option>
        <option value=\"NM\">NM</option>
        <option value=\"NY\">NY</option>
        <option value=\"NC\">NC</option>
        <option value=\"ND\">ND</option>
        <option value=\"OH\">OH</option>
        <option value=\"OK\">OK</option>
        <option value=\"OR\">OR</option>
        <option value=\"PA\">PA</option>
        <option value=\"RI\">RI</option>
        <option value=\"SC\">SC</option>
        <option value=\"SD\">SD</option>
        <option value=\"TN\">TN</option>
        <option value=\"TX\">TX</option>
        <option value=\"UT\">UT</option>
        <option value=\"VT\">VT</option>
        <option value=\"VA\">VA</option>
        <option value=\"WA\">WA</option>
        <option value=\"WV\">WV</option>
        <option value=\"WI\">WI</option>
        <option value=\"WY\">WY</option>
</select>";
}
sub stripWhitespace
{
	my $line = $_[0];
	$line =~ s/^\s+//;
	$line =~ s/\s+$//;
	return $line;
}
return 1;
