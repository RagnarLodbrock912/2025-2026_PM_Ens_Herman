#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

void swapSort(vector<int>& arr) {
    for(int i = 0; i < arr.size(); i++) {
        for(int j = i; j < arr.size(); j++) {
            if(arr[i] > arr[j]) {
                int s = arr[i];
                arr[i] = arr[j];
                arr[j] = s;
            }
        }
    }
}

int main () 
{
    ifstream in("../input.txt");
    ofstream out("../output.txt");

    if (!in.is_open() || !out.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    int n;
    in >> n;
    vector<int> mas(n);

    for (int i = 0; i < n; i++)
        in >> mas[i];

    swapSort(mas);

    for (int i = 0; i < n; i++)
        out << mas[i] << " ";

    return 0;
}
