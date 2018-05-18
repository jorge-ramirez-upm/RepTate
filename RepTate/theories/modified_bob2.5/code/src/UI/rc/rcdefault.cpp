/*
rcdefault.cpp : This file is part bob-rheology (bob) 
bob-2.5 : rheology of Branch-On-Branch polymers
Copyright (C) 2006-2011, 2012 C. Das, D.J. Read, T.C.B. McLeish
 
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details. You can find a copy
  of the license at <http://www.gnu.org/licenses/gpl.txt>
*/

/* set default values first */
void rcdefault(void)
{
  extern int GenPolyOnly, OutMode, PrefMode, ReptScheme, CalcNlin, PrioMode;
  extern int NumNlinStretch, DefinedMaxwellModes, CalcGPCLS, GPCNumBin, GPCPolyMult;

  extern double Alpha, PSquare, TStart, DtMult, RetLim, FreqMax, FreqMin, FreqInterval;
  extern double StretchBinWidth, NlinAvDt, MaxwellInterval, NlinAvInterval;

  GenPolyOnly = CalcNlin = DefinedMaxwellModes = CalcGPCLS = -1;
  OutMode = PrioMode = 0;
  PrefMode = ReptScheme = 1;
  GPCNumBin = 50;
  GPCPolyMult = 50;
  NumNlinStretch = 20;

  FreqMax = 1.0e8;
  FreqMin = 1.0e-3;
  FreqInterval = 1.1;
  MaxwellInterval = 2.0;
  NlinAvInterval = 1.02;
  Alpha = 1.0;
  PSquare = 0.0250;
  TStart = 1.0e-4;
  extern double cur_time;
  cur_time = TStart;

  DtMult = 1.0050;
  RetLim = 0.0;
  StretchBinWidth = 1.25;
  NlinAvDt = 1.10;
  extern int ForceGPCTrace;
  ForceGPCTrace = 0;

  extern int LateRouse, LtRsActivated;
  LateRouse = 1;
  LtRsActivated = 1;
  extern double LtRsFactor;
  LtRsFactor = 42420.0;

  extern int Snipping;
  Snipping = -1;
  extern int NlinPrep;
  NlinPrep = -1;
  extern double SnipTime;
  SnipTime = 0;
  extern double FlowTime;
  FlowTime = 0;
  extern int FlowPriority;
  FlowPriority = -1;
  extern int SlavePhiToPhiST;
  SlavePhiToPhiST = 1;
}
