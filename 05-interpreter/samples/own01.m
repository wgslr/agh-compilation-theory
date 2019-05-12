N = 4;
M = 5;
for i = 1:N {
    i += 3;
    print "first for";
    for j = i:M {
        print i, j;
        continue;
    }
    if (i > 2)
        break;
}


for a = 3:5
    b = a;

{
    e = "naked block";
}
