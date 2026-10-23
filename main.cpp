#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <string>
using namespace std ;
void passsave(string &pass){
	ofstream outFile("pass.txt",ios::app);
        if (!outFile) {
         cerr << "Error opening file!" << endl;
		 return; 
		 }
        outFile <<pass<<endl;
        outFile.close();
}
void passgen(string &pass,string charc,int lenght){
	int len=0;
	int size=static_cast<int>(charc.length());
	if (size == 0 || lenght <= 0) return;
	int n;
	while(len<lenght){
		n=rand() % size;
		pass=charc[n]+pass;
		len++;
	}
	passsave(pass);
	
}
void presave(){
	ifstream infile("pass.txt");
	if(!infile){
        cerr << "Error opening file!" << endl;
        return;
	}
	string line;
	while(getline(infile,line))
	cout<<line<<endl;
	infile.close();
	
}



int main(){
	srand(time(0));
	string pass;
	string upC="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	string lC="abcdefghijklmnopqrstuvwxyz";
	string num="0123456789";
	string ch= "!@#$%^&*()-_=+[]{}|;:,.<>?";
	string charc=upC+lC+num+ch;
	char op;
	int len;
	cout<<"Do you want pre saved passwords(p) or new(n) ? ";
	cin>>op;
	switch(op){
		case 'n':
		case 'N':{
				cout<<"Enter the length of password you want : ";
            	cin>>len;
	            if (!cin || len <= 0 || len > 4096) {
	                cerr << "Password length must be a number from 1 to 4096." << endl;
	                return 1;
	            }
	            passgen(pass,charc,len);
	            cout<<endl<<"Your password is : "<<pass;
			break;
		}
		case 'p':
		case 'P':{
			presave();
			
			
			break;
		}	
	}

	
	
	
	
	
	return 0;
}