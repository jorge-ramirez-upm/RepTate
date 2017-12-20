
  Ran3Inext,Ran3Inextp: integer;
  Ran3Ma: ARRAY [1..55] OF real;
  iy3:integer;

def abs(x):
    return x if x >= 0 else -x 

def ran3(VAR idum: integer):
# (* CONST
#       MBIG = 1000000000;  MSEED=161803398;  MZ=0;  FAC=1.0e-9;
# VAR
#       i,ii,k,mj,mk: longint; *)
    MBIG = 4.0e6;
    MSEED = 1618033.0;
    MZ = 0.0;
    FAC = 2.5e-7;
    # VAR
    # i,ii,k: integer;
    # mj,mk: real;
    if idum < 0:
        mj = MSEED + idum;
        if mj >= 0.0:
            mj = mj - MBIG * np.trunc(mj / MBIG)
        else:
            mj = MBIG - abs(mj) + MBIG * np.trunc(abs(mj) / MBIG);
    # (*    mj = mj MOD MBIG; *)
        Ran3Ma[55] = mj;
        mk = 1;
        for i in range (54) 1 TO 54 DO BEGIN
            ii = 21*i MOD 55;
            Ran3Ma[ii] = mk;
            mk = mj-mk;
            IF mk < MZ THEN mk = mk+MBIG;
            mj = Ran3Ma[ii]
        END;
        FOR k = 1 TO 4 DO BEGIN
            FOR i = 1 TO 55 DO BEGIN
                Ran3Ma[i] = Ran3Ma[i]-Ran3Ma[1+((i+30) MOD 55)];
                IF Ran3Ma[i] < MZ THEN Ran3Ma[i] = Ran3Ma[i]+MBIG
            END
        END;
        Ran3Inext = 0;
        Ran3Inextp = 31;
        idum = 1
    END;
    Ran3Inext = Ran3Inext+1;
    IF Ran3Inext = 56 THEN
        Ran3Inext = 1;
    Ran3Inextp = Ran3Inextp+1;
    IF Ran3Inextp = 56 THEN Ran3Inextp = 1;
    mj = Ran3Ma[Ran3Inext]
                -Ran3Ma[Ran3Inextp];
    IF mj < MZ THEN mj = mj+MBIG;
    Ran3Ma[Ran3Inext] = mj;
    ran3 = mj*FAC
    END;


    end.