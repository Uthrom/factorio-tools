#!/usr/bin/env perl
use strict;
use warnings;

my ($infile, $outfile) = @ARGV;

if (not defined $infile) {
  die "Missing input file";
}

if (not defined $outfile) {
  die "Missing output file";
}

open(my $in, "<", $infile) or die "Can't open input file: $!";
open(my $out, ">", $outfile) or die "Can't open output file: $!";

while (my $line = <$in>) {

    $line =~ s/;return _;end/\n;return _;end\n/g;
    $line =~ s/do local _=/\ndo local _=/g;
    $line =~ s/{entity={/\n    {entity={/g;
    $line =~ s/\[(.*?)\]/\n    \[$1\]/g;
    $line =~ s/entitytarget=0x[0-9a-f\.p+]+/entitytarget=0x[0-9a-f\.p+]+", b"entitytarget=0xdeadbeef/g;

    print $out $line;
}

