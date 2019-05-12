N = 32;

for N = 1 : N / 2 {
    if ((N / 2) * 2 == N)
        continue;
    print N;

    if (N > 12) {
        break;
    }
}


x = "a string";
{
    x = 100;
    print x;
}

print x;
