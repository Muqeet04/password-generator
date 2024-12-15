#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>
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
	int size=charc.length();
	int n;
	while(len<lenght){
		n=rand();
		if(n<0||n>88)
		{
			continue;
		}
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
				cout<<"Enter the Minimum lenght of password you want : ";
            	cin>>len;
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