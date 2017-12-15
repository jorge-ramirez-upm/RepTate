# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http:#blogs.upm.es/compsoftmatter/software/reptate/
# https:#github.com/jorge-ramirez-upm/RepTate
# http:#reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Daniel Read, d.j.read@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module BinsAndBob
 provides routines for binning molecular information calculating averages etc.

 also provides routines for generating required information for BoB
 and deciding whether to save polymers for BoB output

"""
import numpy as np
from PolyBits import PolyBits

class BinsAndBob(PolyBits):

    def __init__(self):
        super().__init__()
        self.self.multi_wt = np.zeros((self.MAX_MWD_BINS))
        self.self.multi_avbr = np.zeros((self.MAX_MWD_BINS))
        self.self.multi_wmass = np.zeros((self.MAX_MWD_BINS))
        self.self.multi_avg = np.zeros((self.MAX_MWD_BINS))
        self.multi_lgmid = np.zeros((self.MAX_MWD_BINS))


    def molbin(self, n):
        """Call this procedure to calculate current averages
    and MWD for polymers made in distribution n"""
        # var i,i1,ibin:integer
        # wttot,m_w,m_n,brav,lgstep,lgmin,lgmax,cplen:double

        self.react_dist[n].nummwdbins = np.min((self.react_dist[n].nummwdbins, self.MAX_MWD_BINS))
        # first find largest and smallest polymer
        lgmax = 0.0
        lgmin = 1.0e80

        i = self.react_dist[n].first_poly
        while True:
            cplen = self.br_poly[i].tot_len
            lgmax = np.max((lgmax, cplen))
            lgmin = np.min((lgmin, cplen))
            i=self.br_poly[i].nextpoly
            if i == 0:
                break

        lgmax = np.log10((lgmax*1.01) * self.react_dist[n].monmass)
        lgmin = np.log10((lgmin/1.01) * self.react_dist[n].monmass)
        lgstep = (lgmax - lgmin)/self.react_dist[n].nummwdbins

        #initialise bins and other counters
        for ibin in range (self.react_dist[n].nummwdbins): #1 to self.react_dist[n].nummwdbins 
            self.react_dist[n].wt[ibin] = 0.0
            self.react_dist[n].avbr[ibin] = 0.0
            self.react_dist[n].avg[ibin] = 0.0
            self.react_dist[n].wmass[ibin] = 0.0

        wttot = 0.0
        m_w = 0.0
        m_n = 0.0
        brav = 0.0

        # the assumption here is that polymers have been created on a weight basis
        i = self.react_dist[n].first_poly
        while True:
            cplen = self.br_poly[i].tot_len * self.react_dist[n].monmass
            ibin = np.trunc((np.log10(cplen) - lgmin)/lgstep) + 1 
            wttot += 1
            m_w = m_w + cplen
            m_n = m_n + 1.0/cplen
            brav = brav + self.br_poly[i].num_br / self.br_poly[i].tot_len
            if (ibin <=  self.react_dist[n].nummwdbins) and (ibin > 0):
                self.react_dist[n].wt[ibin] = self.react_dist[n].wt[ibin] + 1.0
                self.react_dist[n].avbr[ibin] = self.react_dist[n].avbr[ibin] + self.br_poly[i].num_br
                self.react_dist[n].avg[ibin] = self.react_dist[n].avg[ibin] + self.br_poly[i].gfactor
                self.react_dist[n].wmass[ibin] = self.react_dist[n].wmass[ibin] + self.br_poly[i].tot_len
            i = self.br_poly[i].nextpoly
            if i == 0:
                break

        # finalise bin data - ready for plotting
        for ibin in range (self.react_dist[n].nummwdbins): # 1 to self.react_dist[n].nummwdbins
            self.react_dist[n].avbr[ibin] = self.react_dist[n].avbr[ibin] / (self.react_dist[n].wmass[ibin] + 1.0e-80) * 500.0
            self.react_dist[n].avg[ibin] = self.react_dist[n].avg[ibin] / (self.react_dist[n].wt[ibin] + 1.0e-80)
            self.react_dist[n].wt[ibin] = self.react_dist[n].wt[ibin] / lgstep / wttot
            self.react_dist[n].lgmid[ibin] = lgmin + ibin*lgstep - 0.5*lgstep

        self.react_dist[n].m_w = m_w/wttot
        self.react_dist[n].m_n = wttot/m_n
        self.react_dist[n].brav = brav/wttot * 500.0



    def multimolbin(self, reqbins, weights, inmix):
        """ 
        Call this procedure to calculate current averages
        and MWD for all polymers made in all distributions
        with weights contained in weights array, and whether "in the mix" contained
        in inmix array
        """
        # var i,i1,ibin,n:integer
        # wttot,m_w,m_n,brav,lgstep,lgmin,lgmax,cplen,wtpoly:double
        self.multi_nummwdbins = np.min((reqbins, self.MAX_MWD_BINS))

        # first find largest and smallest polymer
        lgmax = 0.0
        lgmin = 1.0e80

        for n in range (1, 11): #1 to 10
            if inmix[n - 1] and (weights[n - 1] > 0.0):
                i = self.react_dist[n].first_poly
                while True:
                    cplen = self.br_poly[i].tot_len * self.react_dist[n].monmass
                    lgmax = np.max((lgmax, cplen))
                    lgmin = np.min((lgmin, cplen))
                    i = self.br_poly[i].nextpoly
                    if i == 0:
                        break

        lgmax = np.log10(lgmax * 1.01)
        lgmin = np.log10(lgmin / 1.01)
        lgstep = (lgmax - lgmin)/self.multi_nummwdbins

        #initialise bins and other counters
        for ibin in range(self.multi_nummwdbins):
            self.multi_wt[ibin] = 0.0
            self.multi_avbr[ibin] = 0.0
            self.multi_avg[ibin] = 0.0
            self.multi_wmass[ibin] = 0.0

        wttot = 0.0
        m_w = 0.0
        m_n = 0.0
        brav = 0.0

        # the assumption here is that polymers have been created on a weight basis
        for n in range (1, 11): #1 to 10
            if inmix[n - 1] and (weights[n - 1] > 0.0):
                i = self.react_dist[n].first_poly
                wtpoly = weights[n-1] / self.react_dist[n].npoly
                while True:
                    cplen = self.br_poly[i].tot_len*self.react_dist[n].monmass
                    ibin = np.trunc((np.log10(cplen) - lgmin) / lgstep) + 1 
                    wttot = wttot + wtpoly
                    m_w = m_w + cplen * wtpoly
                    m_n = m_n + wtpoly / cplen
                    brav = brav + self.br_poly[i].num_br / self.br_poly[i].tot_len * wtpoly
                    if (ibin <=  self.multi_nummwdbins) and (ibin > 0):
                        self.multi_wt[ibin] = self.multi_wt[ibin] + wtpoly
                        self.multi_avbr[ibin] = self.multi_avbr[ibin] + self.br_poly[i].num_br * wtpoly
                        self.multi_avg[ibin] = self.multi_avg[ibin] + self.br_poly[i].gfactor * wtpoly
                        self.multi_wmass[ibin] = self.multi_wmass[ibin] + self.br_poly[i].tot_len * wtpoly
                    i = self.br_poly[i].nextpoly
                    if i == 0:
                        break

        # finalise bin data - ready for plotting
        for ibin in range (self.multi_nummwdbins):
            self.multi_avbr[ibin] = self.multi_avbr[ibin] / (self.multi_wmass[ibin] + 1.0e-80) * 500.0
            self.multi_avg[ibin] = self.multi_avg[ibin] / (self.multi_wt[ibin] + 1.0e-80)
            self.multi_wt[ibin] = self.multi_wt[ibin] / lgstep / wttot
            multi_lgmid[ibin] = lgmin + ibin * lgstep - 0.5*lgstep

        self.multi_m_w = m_w/wttot
        self.multi_m_n = wttot/m_n
        self.multi_brav = brav/wttot * 500.0


        
    def bobinit(self, n):
        """Call this before making any polymers"""
        for i in range (self.react_dist[n].numbobbins):
            self.react_dist[n].numinbin[i] = 0
            self.react_dist[n].nsaved = 0


    def bobcount(self, m, n):
        """
        checks to see whether or not to save this polymer 
        (polymer m, from self.react_dist n)
        """
        ibin = np.trunc((np.log10(self.br_poly[m].tot_len * self.react_dist[n].monmass) - self.react_dist[n].boblgmin) / (self.react_dist[n].boblgmax - self.react_dist[n].boblgmin) * self.react_dist[n].numbobbins) + 1
        ibin = np.min((np.max((1, ibin)), self.react_dist[n].numbobbins))
        self.react_dist[n].numinbin[ibin] = self.react_dist[n].numinbin[ibin] + 1
        if self.react_dist[n].numinbin[ibin] <= self.react_dist[n].bobbinmax:  #  check to see whether to "save" the polymer
            self.br_poly[m].saved = True
            self.br_poly[m].bin = ibin
            self.react_dist[n].nsaved = self.react_dist[n].nsaved + 1
        else:
            self.br_poly[m].saved = False
            self.br_poly[m].bin = 0
            self.return_poly_arms(m)


    def polyconfwrite(self, n, Fname):
        # var i,atally,numarms,anum:integer
        #     first,tL1, tL2, tR1, tR2, m1,mc, npoly: integer
        #     F: TextFile
        #     enrich,polywt,armwt,armz,N_e:double

        # TODO: change this bit to comply with Reptate standards 
        AssignFile(F, Fname)
        Rewrite(F)
        self.react_dist[n].N_e = self.react_dist[n].M_e / self.react_dist[n].monmass
        # opening lines
        writeln(F, 'reactpol')
        writeln(F, self.react_dist[n].N_e:12)
        writeln(F, self.react_dist[n].nsaved)


        atally = 0

        # loop through polymers, writing output
        npoly = self.react_dist[n].npoly
        N_e = self.react_dist[n].N_e
        i = self.react_dist[n].first_poly
        while True
            if self.br_poly[i].saved:

                if self.react_dist[n].numinbin[self.br_poly[i].bin] <=  self.react_dist[n].bobbinmax:
                    enrich = 1.0
                else:
                    enrich = self.react_dist[n].numinbin[self.br_poly[i].bin] / self.react_dist[n].bobbinmax

                polywt = enrich/npoly

                if self.br_poly[i].num_br == 0: #it's a linear polymer
                    writeln(F,2) #TODO
                    atally = atally + 2
                    first = self.br_poly[i].first_end
                    armwt = 0.5*self.arm_pool[first].arm_len / self.br_poly[i].tot_len / npoly * enrich
                    armz = 0.5*self.arm_pool[first].arm_len / N_e
                    writeln(F, -1:2,-1:3,1:2,-1:3,armz:12,' ',armwt:15) #TODO
                    writeln(F, 0:1,-1:3,-1:3,-1:3,armz:12,' ',armwt:15) #TODO
                else: # it's a branched polymer
                    numarms = 2*self.br_poly[i].num_br + 1
                    writeln(F,numarms)  #number of arms #TODO
                    atally = atally + numarms
                    first = self.br_poly[i].first_end

                    #renumber segments starting from zero
                    m1 = first
                    anum = 0
                    while True:
                        self.arm_pool[m1].armnum = anum
                        m1 = self.arm_pool[m1].down
                        anum = anum+1
                        if m1 == first:
                            break

                    # now do output - loop over arms
                    m1 = first
                    while True:
                        armwt = self.arm_pool[m1].arm_len / self.br_poly[i].tot_len / npoly*enrich
                        armz = self.arm_pool[m1].arm_len / N_e
                        if self.arm_pool[m1].L1  ==  0:
                            tL1 = -1
                        else:
                            mc = np.abs(self.arm_pool[m1].L1)
                            tL1 = self.arm_pool[mc].armnum
                       
                        if self.arm_pool[m1].L2 == 0:
                            tL2 = -1
                        else:
                            mc = np.abs(self.arm_pool[m1].L2)
                            tL2 = self.arm_pool[mc].armnum
                       
                        if self.arm_pool[m1].R1 == 0:
                            tR1 = -1
                        else:
                            mc = np.abs(self.arm_pool[m1].R1)
                            tR1 = self.arm_pool[mc].armnum
                       
                        if self.arm_pool[m1].R2 == 0:
                            tR2 = -1
                        else:
                            mc = np.abs(self.arm_pool[m1].R2)
                            tR2 = self.arm_pool[mc].armnum
                       
                        writeln(F,tL1,' ',tL2,' ',tR1,' ',tR2,' ',armz:12,' ',armwt:15) #TODO
                        m1 = self.arm_pool[m1].down
                        
                        if m1 == first:  #end output loop over arms
                            break
                # end of if (it's a linear or branched polymer )


            #end of "if saved"
            i = self.br_poly[i].nextpoly
            if  i == 0:    #end of loop over polymers
                break
        CloseFile(F)


    def multipolyconfwrite(self, Fname, weights, inmix, numsaved):
        """version for mixtures"""
        # var i,atally,numarms,anum,n,nmix:integer
        #     first,tL1, tL2, tR1, tR2, m1,mc, npoly: integer
        #     F: TextFile
        #     enrich,polywt,armwt,armz,N_e,N_e_av,distwt:double

        # TODO: change this bit to comply with Reptate standards 
        AssignFile(F, Fname)
        Rewrite(F)

        # count polymers over all distributions
        numsaved = 0
        nmix = 0
        N_e_av = 0

        for n in range (1, 11):
            if inmix[n - 1]:
                self.react_dist[n].N_e = self.react_dist[n].M_e / self.react_dist[n].monmass
                N_e_av = N_e_av + self.react_dist[n].N_e
                nmix += 1
                numsaved = numsaved + self.react_dist[n].nsaved

        N_e_av = N_e_av/nmix

        # opening lines
        #TODO: modif this
        writeln(F, 'reactmix')
        writeln(F,N_e_av:12)
        writeln(F,numsaved )

        atally = 0

        # now loop through distributions writing output
        for n in range (1, 11):
            if inmix[n-1]:
                distwt = weights[n-1]

                # loop through polymers, writing output
                npoly = self.react_dist[n].npoly
                N_e = self.react_dist[n].N_e
                i = self.react_dist[n].first_poly
                while True:
                    if self.br_poly[i].saved:
                        if self.react_dist[n].numinbin[self.br_poly[i].bin] <= self.react_dist[n].bobbinmax:
                            enrich = 1.0
                        else:
                            enrich = self.react_dist[n].numinbin[self.br_poly[i].bin] / self.react_dist[n].bobbinmax
                        polywt = enrich / npoly * distwt

                        if self.br_poly[i].num_br == 0: #it's a linear polymer
                            writeln(F,2)
                            atally = atally + 2
                            first = self.br_poly[i].first_end
                            armwt = 0.5*self.arm_pool[first].arm_len / self.br_poly[i].tot_len * polywt
                            armz = 0.5*self.arm_pool[first].arm_len / N_e
                            writeln(F, -1:2,-1:3,1:2,-1:3,armz:12,' ',armwt:15)
                            writeln(F, 0:1,-1:3,-1:3,-1:3,armz:12,' ',armwt:15)
                        else: # it's a branched polymer
                            numarms = 2*self.br_poly[i].num_br + 1
                            writeln(F,numarms)  #number of arms
                            atally = atally + numarms
                            first = self.br_poly[i].first_end

                            #renumber segments starting from zero
                            m1 = first
                            anum = 0
                            while True:
                                self.arm_pool[m1].armnum = anum
                                m1 = self.arm_pool[m1].down
                                anum = anum + 1
                                if m1  == first:
                                    break

                            # now do output - loop over arms
                            m1 = first
                            while True:
                                armwt = self.arm_pool[m1].arm_len / self.br_poly[i].tot_len * polywt
                                armz = self.arm_pool[m1].arm_len / N_e
                                if self.arm_pool[m1].L1 == 0:
                                    tL1 = -1
                                else:
                                    mc = np.abs(self.arm_pool[m1].L1)
                                    tL1 = self.arm_pool[mc].armnum
                                
                                if self.arm_pool[m1].L2 == 0:
                                    tL2 = -1
                                else:
                                    mc = np.abs(self.arm_pool[m1].L2)
                                    tL2 = self.arm_pool[mc].armnum
                                
                                if self.arm_pool[m1].R1 == 0:
                                    tR1 = -1
                                else:
                                    mc = np.abs(self.arm_pool[m1].R1)
                                    tR1 = self.arm_pool[mc].armnum
                                
                                if self.arm_pool[m1].R2 == 0:
                                    tR2 = -1
                                else:
                                    mc = np.abs(self.arm_pool[m1].R2)
                                    tR2 = self.arm_pool[mc].armnum
                                
                                writeln(F,tL1,' ',tL2,' ',tR1,' ',tR2,' ',armz:12,' ',armwt:15)

                                m1 = self.arm_pool[m1].down

                                if m1 == first:  #end output loop over arms
                                    break
                        # end of if (it's a linear or branched polymer )
                    #end of "if saved"
                    i = self.br_poly[i].nextpoly
                    if i == 0:    #end of loop over polymers
                        break
            # end of loop over distributions
        CloseFile(F) # TODO: modify
        