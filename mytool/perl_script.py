def generator(cui_1, cui_2):
    f = open('run.pl', 'w')
    code1 = '''use UMLS::Interface;
use UMLS::Similarity::lch;
use UMLS::Similarity::path;

my $umls = UMLS::Interface->new(); 
die "Unable to create UMLS::Interface object.\\n" if(!$umls);

my $lch = UMLS::Similarity::lch->new($umls);
die "Unable to create measure object.\\n" if(!$lch);

my $path = UMLS::Similarity::path->new($umls);
die "Unable to create measure object.\\n" if(!$path);
 
my $cui1 = '''
    code2 = ''';
my $cui2 = 
    '''
    code3 = ''';
$ts1 = $umls->getTermList($cui1);
my $term1 = pop @{$ts1};
 
$ts2 = $umls->getTermList($cui2);
my $term2 = pop @{$ts2};
 
my $lvalue = $lch->getRelatedness($cui1, $cui2);
 
my $pvalue = $path->getRelatedness($cui1, $cui2);

print "The lch similarity between $cui1 ($term1) and $cui2 ($term2) is $lvalue\\n";

print "The path similarity between $cui1 ($term1) and $cui2 ($term2) is $pvalue\\n";
    '''
    code_all = code1+cui_1+code2+cui_2+code3
    f.write(code_all)
    f.close()