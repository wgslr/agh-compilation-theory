for i = 1:N {
    if(i<=N/16)
        print i;
    else if(i<=N/8)
        break;
    else if(i<=N/4)
        continue;
    else if(i<=N/2)
        return 0;
}


print 3;
print 4
