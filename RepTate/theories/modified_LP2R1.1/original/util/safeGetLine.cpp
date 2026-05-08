#include <string>
#include <iostream>
#include <algorithm>
/**
  * \file
  * \brief
  * read a nonempty line with either unix or windows style line-ending, discarding anything after a % sign
  *
  * handle line ending with \\n, \\r, \\r\\n, or no line ending
  */

/**
  * Implementation of getline() to handle different line endings.
  * \param[in] is input stream
  * \param[out] t string
  * \return input stream
  */

std::istream& safeGetline_int(std::istream& is, std::string& t)
{
    t.clear();
    std::istream::sentry se(is, true);
    std::streambuf* sb = is.rdbuf();

    for(;;) {
        int c = sb->sbumpc();
        switch (c) {
        case '\n':
            return is;
        case '\r':
            if(sb->sgetc() == '\n')
                sb->sbumpc();
            return is;
        case std::streambuf::traits_type::eof():
            // Also handle the case when the last line has no line ending
            if(t.empty())
                is.setstate(std::ios::eofbit);
            return is;
        default:
            t += (char)c;
        }
    }
}

/**
  * Read a line from the input stream, discard anything after a '%' sign (treat as comment indicator)
  * If the resulting string has no non-space characters and the input stream hasn't reached 
  * the end of file, read the next line. Continue till either the end of file is reached, or a
  * line with some non-empty, non-comment character is found.
  *
  * \param[in] is input stream
  * \param[out] t string
  * \return input stream
  */

std::istream& safeGetline(std::istream& is, std::string& t)
{
bool cont_read=true;
while(cont_read){
if(!safeGetline_int(is, t).eof()){
std::size_t pos=t.find('%');
if(pos != std::string::npos){t=t.substr(0,pos);}
int nd=0;
for(std::size_t i=0; i<t.size(); i++){
 if( (t[i] != ' ') && (t[i] != '\t')){nd++;}
                                     }
if(nd > 0){cont_read=false;}

                                 }
else{cont_read=false;}
                }
return is;
}

/**
  * Read lines with contents like a=b
  * On either side of the equality, space or tabs are removed
  * return the LHS and RHS separately in sL and sR
  *
  * \param[in] is input stream
  * \param[out] sL string containing LHS of some equality
  * \param[out] sR string containing RHS of some equality
  * \return input stream
  */
 
std::istream& readEquality(std::istream& is, std::string& sL, std::string& sR)
{
bool cont_read=true;
std::string t;
while(cont_read){
if(!safeGetline(is, t).eof()){
std::size_t pos=t.find('=');
if(pos != std::string::npos){ // valid equailty
t.erase(remove(t.begin(), t.end(), ' '), t.end());
t.erase(remove(t.begin(), t.end(), '\t'), t.end());
pos=t.find('=');
sL=t.substr(0,pos);
sR=t.substr(pos+1, t.length()-pos-1);
cont_read=false;
                            }

                                 }
else{cont_read=false;}
                }

return is;
}

