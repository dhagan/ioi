#!/usr/bin/perl

################################################################################
#
#       File Name: knowledgebase.cgi
#
#       Purpose: Used for searching the IOI database for related tickets.
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
use DBI;
$REQUIRE_DIR ='modules';
push(@INC, $REQUIRE_DIR) if $REQUIRE_DIR;
require "ioistyle.cgi";
require "ioiquery.cgi";
$cgi = new CGI;
	print $cgi->header();

if (param('short_desc'))
{
	searchRes();
	searchForm();
}
else
{
	searchForm();
}


sub searchForm()
{
	headers();
	background();
	bodyAndLoad();
	tableHead('50%');
	print "<script language='javascript'>
			function checkSubmit()
			{
				if (document.form2.free_text_query.value == '')
				{
					alert('Please enter a phrase to search the knowledgebase with');
				}
			}
			</script>
		   <form name='form2' id='form2' action='searchTickets.cgi' onSubmit='return checkSubmit()'>
		   <tr bgcolor='#B0B0B0'><td><div align='center'>IOI Knowledgebase</div></td></tr>
		   <tr bgcolor='#B0B0B0'><td><div align='center'>Search for any keyword or part of a word.</div></td></tr>
		   <tr><td><div align='center'><input type='text' name='query' value='' size='50'></div></td></tr>
		   <tr><td><div align='center'><input type='checkbox' name='free_text_query' value='Yes'>Free text query - Use for finding particular words in tickets with an unknown order</div></td></tr>
		   <tr><td><div align='center'><input type='submit' name='knowledgebase' value='Search Knowledgebase'><div></td></tr></form></table>";
	end_HTML();
}

#The below method has nothing to do with the searchform above. This only searches automatically for you when you click the link on the page
sub searchRes()
{
	my $dbh = getDBConnection();
	$dbh-> {'LongReadLen'} = 2000000;
	$text = param('short_desc');
	$text =~ s /\\//g;
	$free_text_query = param('free_text_query');
	$statement = "select case_num,short_desc,assigned_to,submitted_by from problem where ";
	headers();
	background();
	bodyAndLoad();
	@text = split(/ /,$text);
	$link_text = $text;
	$link_text =~ s/ /+/g;
	$link_ending = "&query=$link_text" if ($free_text_query ne "Yes");
	$i = 0;
	if ($free_text_query eq "Yes")
	{	
		foreach $word(@text)
		{
			{
			$link_ending = $link_ending . "&query=$word";
			}
			$statement = $statement . "(problem like '%$word%' or short_desc like '%$word%') " if ($i == 0);
			$statement = $statement . "and (problem like '%$word%' or short_desc like '%$word%')" if ($i > 0 );
			$i++;
		}
	}
	else
	{
		$statement = $statement . "problem like '%$text%' or short_desc like '%$text%'";
	}
	#print "$statement";
	$sth = $dbh->prepare($statement);
	$sth->execute();
	
	tableHead('85%');
	print "<tr><td>Ticket #</td><td>Subject</td><td>Assigned To</td><td>Customer Name</td></tr>";
	while (($case_num,$short_desc,$assigned_to,$submitted_by) = $sth->fetchrow_array())
	{
		if ($free_text_query eq "Yes")
		{
			foreach $word(@text)
			{
			$short_desc =~ s/$word/<b><font color='red'>$word<\/font><\/b>/gi;
			}
		}
		else { $short_desc =~ s/$text/<b><font color='red'>$text<\/font><\/b>/gi;}
		$customer = $dbh->prepare("select sub_name from users where sub_login = '$submitted_by'");
		$customer->execute();
		$sub_name = $customer->fetchrow_array();
		$customer->finish();
		push @table, "<tr><td><a href='respondTicket.cgi?viewTicket=yes&case_num=$case_num$link_ending'>$case_num</a></td><td>$short_desc</td><td>$assigned_to</td><td>$sub_name</td></tr>";
	}
	
	print @table if (@table[0] ne "");
	
	print "</table>";
	ioiFont("No search results were found") if (@table[0] eq "");
	end_html();
	
	$sth->finish();
	$dbh->disconnect();
}	