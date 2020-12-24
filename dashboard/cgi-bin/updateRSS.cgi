#!/usr/bin/perl

################################################################################
#
#       File Name: updateRSS.cgi
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

use strict;
use CGI;
use XML::RSS;
use CGI::Carp qw(fatalsToBrowser);
my $REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
my $cgi = new CGI;

#Check for state we are in
if (param('update'))
{
	update();
}
else
{
	changeRSS();
}

#changeRSS gets the current RSS info and allows you to append to it or create a completly new one
sub changeRSS()
{
	my @title = ();
	my @description = ();
	my @link = ();
	my $rss = new XML::RSS(version=>'2.0');
	$rss->parsefile("/Library/WebServer/documents/dashboard/rss/ioi.rss") or die "Could not find rss file";
	foreach my $item(@{$rss->{'items'}})
	{
		push @title, $item->{'title'};
		
		my $link = $item->{'guid'};
		$link =~ s/http:\/\///g;
		push @link, $link;
		push @description, $item->{'description'};
	}
	print $cgi->header();
	headers();
	background();
	print "<script language='javascript'>
	function addRowToTable()
	{
		
		
		var rssForm = document.rss;
		
	  // if there's no header row in the table, then iteration = lastRow + 1
 
	  var titleBox = document.createElement('input');
	  titleBox.setAttribute('type', 'text');
	  titleBox.setAttribute('name', 'title');
	  titleBox.setAttribute('size', '20');
	  titleBox.setAttribute('onKeypress','boxexpand(this)');
	  
	   var linkBox = document.createElement('input');
	  linkBox.setAttribute('type', 'text');
	  linkBox.setAttribute('name', 'link');
	  linkBox.setAttribute('size', '20');
	  linkBox.setAttribute('onKeypress','boxexpand(this)');
	   var descriptionBox = document.createElement('input');
	  descriptionBox.setAttribute('type', 'text');
	  descriptionBox.setAttribute('name', 'description');
	  descriptionBox.setAttribute('size', '20');
	  descriptionBox.setAttribute('onKeypress','boxexpand(this)');
	  
	  var TitleText = document.createTextNode(\"Title\");
	  var LinkText = document.createTextNode(\"Link\");
	  var DescText = document.createTextNode(\"Description\");
	 
	 var table = document.createElement('TABLE');
	 table.setAttribute('border',1);
	 table.setAttribute('width','95%');
	 table.setAttribute('bordercolor','#C0C0C0');
	 table.setAttribute('bgcolor','#909090');
	 table.setAttribute('cellspacing',0);
	 table.setAttribute('cellpadding',5);
	 table.setAttribute('align','center');
	 var row1 = table.appendChild(document.createElement('TR'));
	 var td1 = row1.appendChild(document.createElement('TD'));
	 var td2 = row1.appendChild(document.createElement('TD'));
	 td1.appendChild(TitleText);
	 td2.appendChild(titleBox);
	 var row2 = table.appendChild(document.createElement('TR'));
	 var td1 = row2.appendChild(document.createElement('TD'));
	 var td2 = row2.appendChild(document.createElement('TD'));
	 td1.appendChild(LinkText);
	 td2.appendChild(linkBox);
	 var row3 = table.appendChild(document.createElement('TR'));
	 var td1 = row3.appendChild(document.createElement('TD'));
	 var td2 = row3.appendChild(document.createElement('TD'));
	 td1.appendChild(DescText);
	 td2.appendChild(descriptionBox);
	 rssForm.appendChild(table);
	 
	}
function deleteFeed(feedNum)
{
	var deleteTable = document.getElementById('feed' + feedNum);
	deleteTable.style.display = 'none';
	document.rss.title[feedNum].value = '';
	document.rss.link[feedNum].value = '';
	document.rss.description[feedNum].value = '';
	 
}
function boxexpand(currentBox)

{

boxValue=currentBox.value.length
boxSize=currentBox.size
minNum=20 // Set this to the MINIMUM size you want your box to be.

maxNum=100 // Set this to the MAXIMUM size you want your box to be.
if (boxValue > maxNum)
  {
  }
else

{
  if (boxValue > minNum)
    {
    currentBox.size = boxValue
    }
  else if (boxValue < minNum || boxValue != minNum)
    {
      currentBox.size = minNum
    }
}

}

// End of script //

</script>
 </script>";
	bodyAndLoad();
	print "<form name='rss' id='rss' method='post' action=''>\n";
	for(my $i = 0; $i < @title; $i++)
	{
		print "<tr>\n";
		tableHead('95%',"id='feed$i'");
		print"
		<tr><td>Title</td><td><input type='text' name='title' value='@title[$i]' onKeypress='boxexpand(this)'></td></tr>
		<tr><td>Link</td><td>http://<input type='text' name='link' onKeypress='boxexpand(this)' value='@link[$i]'></td></tr>
		<tr><td>Description</td><td><input type='text' name='description' onKeypress='boxexpand(this)' value='@description[$i]'></td></tr>
		<tr bgcolor='#66CCFF'><td colspan='2'><div align='center'><input type='button' name='delete' value='Delete Feed' onClick='deleteFeed($i)'></div></td></tr>
		</table>";
	}
	print "<div align='center'>
	<input type='button' name='AddRow' value='Add Feed' onClick='addRowToTable();'>
	<input type='submit' name='update' value='Update Feed'><P>New Feeds<p></div></form>";
	end_HTML();
}

sub update()
{
	my @title = param('title');
	my @link = param('link');
	foreach my $title (@title)
	{
		print $title;
	}
	my @description = param('description');
	my $rss = new XML::RSS(version=>'2.0');
	 $rss->channel(title          => 'IO Integration',
               link           => 'http://www.iointegration.com',
               language       => 'en',
               description    => '#1 Integrators',
               copyright      => 'Copyright 2006, IO Integration',
               pubDate        => localtime,
               lastBuildDate  => localtime,
               managingEditor => 'support@iointegration.com',
               webMaster      => 'support@iointegration.com'
               );
	
	for (my $i = 0; $i < @title; $i++)
	{
		 $rss->add_item(title => @title[$i],
        # creates a guid field with permaLink=true
        permaLink  => "http://@link[$i]",
                # alternately creates a guid field with permaLink=false
        # guid     => "gtkeyboard-0.85
        description => @description[$i]
		);
	}
	$rss->save("/Library/WebServer/Documents/dashboard/rss/ioi.rss") or die $!;
	print $cgi->header();
		foreach my $title (@title)
	{
		print $title;
	}
	print "Saved successfully";
}
	