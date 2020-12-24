#!/usr/bin/perl

################################################################################
#
#       File Name: ioiengineering.cgi
#
#       Purpose: This file is used for 
#
#       Copyright © 2006 IOIntegration Inc. Internal use only.
#
#       Revision History:
#
#       Date            Author          Action
#       ----            ------          ------
#       02/02/2006      M. Smith        Created this file
#
################################################################################

use CGI::Carp qw(fatalsToBrowser);
use CGI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";


#Get the users state

if (param('newproject'))
{
	newProject();
}
elsif (param('updateproject'))
{
	updateProject();
}
elsif (param('finishedprojects'))
{
	finishedprojects();
}
else
{
	viewprojects();
}

sub viewprojects()
{
	print header();
	$statement = "SELECT * FROM project WHERE project_status  != 'Completed'";
	$dbh = getDBConnection();
	$sth = $dbh->prepare($statement);
	$sth->execute();
	$i = 0;
	while(($project_id,$project_priority,$project_name, $project_details,$project_eta,$project_finished,$project_value,$osx,$windows,$linux,$polish,$module,$encode,$installer,$documentation,$graphics) = $sth->fetchrow_array())
	{
		$flashString .= "&id$i=$project_id&project_name$i=$project_name&priority$i=$project_priority&eta$i=$project_eta&$finished$i=$project_finished&value$i=$project_value&osx$i=$osx&windows$i=$windows&linux$i=$linux&polish$i=$polish&module$i=$module&encode$i=$encode&installer$i=$installer&documentation$i=$documentation&graphics$i=$graphics";
		$i++;
	}
	print $flashString, "&";
}
# sub viewprojects()
# {
# 	print header();
# 	headers();
# 	background();
# 	bodyAndLoad();
# 	tableHead('95%');
# 	print "<tr bgcolor='#B0B0B0'><td>Priority</td><td>Project Name</td><td>Details</td><td>ETA</td><td>Value</td><td>OSX</td><td>Windows</td><td>Linux</td><td>polish</td><td>Module</td><td>Encode</td><td>Installer</td><td>Documentation</td><td>Graphics</td></tr>";
# 	$statement = "SELECT * FROM project WHERE project_status  != 'Finished'";
# 	$dbh = getDBConnection();
# 	$sth = $dbh->prepare($statement);
# 	$sth->execute();
# 	while(($project_id,$project_priority,$project_name, $project_details,$project_eta,$project_finished,$project_value,$osx,$windows,$linux,$polish,$module,$encode,$installer,$documentation,$graphics) = $sth->fetchrow_array())
# 	{
# 		print "<tr>
# 				<td>$project_priority</td>
# 				<td>$project_name</td>
# 				<td>$project_details</td>
# 				<td>$project_eta</td>
# 				<td>$project_value</td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($osx ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($windows ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($linux ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($polish ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($module ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($encode ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($installer ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($documentation ==1); print "></td>
# 				<td><input type='checkbox' "; print "CHECKED" if ($graphics ==1); print "></td>
# 			</tr>";
# 		}
# 		print "</table>";
# }
# 			
# 	