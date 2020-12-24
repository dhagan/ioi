#!/usr/bin/perl

################################################################################
#
#       File Name: deleteTickets.cgi
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
$cgi = new CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
my $dbh = getDBConnection();

print $cgi->header();
print $cgi->start_html();
print "<style type='text/css'>
		<!--
		body {
			background-color: #C0C0C0;
		}
		
		-->
		</style>";

@case_nums = $cgi->param('selrow');
print "<div align='center'>The following Tickets have been deleted from the Helpdesk:</div><p>
<script language='JavaScript'>

</script>";

foreach $case_num(@case_nums)
{
	print "<div align='center'>$case_num</div><p>";
		$update = "Update problem SET problem='',assigned_to='',status='Deleted',xinet_ticket_num='',bug_ticket_num='' where case_num = '$case_num'";
		$sth = $dbh->prepare($update);
		$sth->execute();
}
print "<div align='center'>Click <a href = 'FilterTickets.cgi'>here</a> to go back to the filter tickets page</center>";
$dbh->commit();
  $dbh->disconnect();
print $cgi->end_html();