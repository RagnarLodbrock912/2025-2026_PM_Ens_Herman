#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>

using namespace std;

void shellSort(vector<int>& arr) {
    int d = round(arr.size() / 2);
    while (d > 0) {
        for (int i = 0; i < arr.size() - d; i++) {
            if (arr[i] > arr[i + d]) {
                    int s = arr[i];
                    arr[i] = arr[i + d];
                    arr[i + d] = s;   
                }
            int t = i;
            while (t - d >= 0) {
                if (arr[t - d] > arr[t]) {
                    int s = arr[t];
                    arr[t] = arr[t - d];
                    arr[t - d] = s; 
                    t -= d;
                }
                else
                    break;
            }
        }
        d = round(d / 2);   
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

    shellSort(mas);

    for (int i = 0; i < n; i++)
        out << mas[i] << " ";

    return 0;
}
