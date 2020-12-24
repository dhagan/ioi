#!/usr/bin/perl

################################################################################
#
#       File Name: assignTickets.cgi
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

use DBI;
use CGI;
use MIME::Lite;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
my $dbh = getDBConnection();
$cgi = new CGI;
print $cgi->header();
print "
<style type=\"text/css\">
<!--
body {
	background-color: #C0C0C0;
}

-->
</style>";
@case_nums = $cgi->param('selrow');
$case_nums[++$#case_nums] = $cgi->param('case_num') if($cgi->param('case_num'));
%alreadyAssigned = ();
$assigned_to = $cgi->param('assigned_to');
$sth = $dbh->prepare("SELECT sa_e_mail, sa_name FROM staff WHERE sa_login = '$assigned_to'");
$sth->execute();
($sa_email,$sa_name) = $sth->fetchrow_array();

print "<style type='text/css'>
		<!--
		body {
			background-color: #C0C0C0;
		}
		
		-->
		</style>";

print "<center><font color='#C0C0C0'>The following tickets have been assigned to $assigned_to:</font><p>";
foreach $case_num(@case_nums)
{
	if(!$cgi->param('skipCheck'))
	{
		$sth = $dbh->prepare("SELECT assigned_to FROM problems WHERE case_num = '$case_num'");
		$sth->execute();
		($assigned) = $sth->fetchrow_array();
		if ($assigned ne "nobody")
		{
			$alreadyAssigned{$case_num} = $assigned;
			next;
		}
	}
print "<font color = '#C0C0C0'>$case_num</font><p>";
$sth = $dbh->prepare("SELECT short_desc, submitted_by, prob_prod_link FROM problems WHERE case_num = '$case_num'");
$sth->execute();
($short_desc,$submitted_by,$prob_prod_link) = $sth->fetchrow_array();
$sth = $dbh->prepare("SELECT prod_name FROM product WHERE prod_case_num = '$prob_prod_link'");
$sth->execute();
$prod_name = $sth->fetchrow_array();
$sth = $dbh->prepare("SELECT sub_name FROM users WHERE sub_login = '$submitted_by'");
$sth->execute();
$sub_name = $sth->fetchrow_array();
$sth = $dbh->prepare("UPDATE problems SET assigned_to = '$assigned_to' WHERE case_num = '$case_num'");
$sth->execute();
$dbh->commit();


		$email = MIME::Lite->new(
			From => "support\@iointegration.com", To =>$sa_email, Subject =>"Ticket $case_num from $sub_name regarding $prod_name requires attention", Type => 'multipart/mixed');
			$email->attach( Type =>'TEXT', Data => "Hey $sa_name \n\n A ticket has been opened for $sub_name has been assigned to you.\n\n Ticket Subject: $short_desc. \n\n Please assist them as soon as possible. (Or let Bill or Nige know ASAP ifyou are unable to take this call)" );
			$email->replace("Date","");
			#$email->add("Return Path", "hdtest\@iointegration.com");
			#$email->add("Reply-To","hdtest\@iointegration.com");
			#$email->send_by_smtp('mail.iointegration.com','matt','ioimail');
}
if (!$cgi->param('skipCheck'))
{
print "<form name='form1' action= '' >
	   <input type='hidden' name='skipCheck' value='yes'>
	   <input type='hidden' name='assigned_to' value='$assigned_to'";
	   ioiFont("The following tickets are already assigned, check the ones that you would like to reassign to yourself");
	   tableHead('95%');
	   print "<tr><td>Ticket #</td><td>Currently Assigned To</td><td>Subject</td></tr>";
	   while( my ($case_num,$assigned_to) = each(%alreadyAssigned))
	   {
	   		$sth = $dbh->prepare("SELECT short_desc FROM problem WHERE case_num = '$case_num'");
	   		$sth->execute();
	   		($subject) = $sth->fetchrow_array();
			print "<tr><td><input type='checkBox' name='selrow' value='$case_num'>$key</td>
			<td>$assigned_to</td><td>$subject</td></tr>"
		}
		print "<tr><td colspan='3'><center><input type='submit' name='Assign' value='Assign'></center></td></tr></table></form>";
}
print $cgi->end_html();
$dbh->disconnect();