N = 32;

# skip even numbers, end iteration when over 12
for N = 1 : N / 2 {
    if ((N / 2) * 2 == N)
        continue;
    print N;

    if (N > 12) {
        break;
    }
}

