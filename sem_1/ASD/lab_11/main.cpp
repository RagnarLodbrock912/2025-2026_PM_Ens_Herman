#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>

using namespace std;

vector<int> quickSort(vector<int>& arr) {
    if(arr.size() == 2) {
        if (arr[0] > arr[1]) {
                int s = arr[0];
                arr[0] = arr[1];
                arr[1] = s;
        }
        return arr;   
    }
    else if (arr.size() < 2)
        return arr;
    else {
        int fixed = arr[round(arr.size() / 2)];
        vector<int> left, right;
        for (int i = 0; i < arr.size(); i++) {
            if(i == round(arr.size() / 2))
                continue;
            else if (arr[i] < fixed)
                left.push_back(arr[i]);
            else
                right.push_back(arr[i]);
        }
        left = quickSort(left);
        right = quickSort(right);
        arr.clear();
        arr.insert(arr.end(), left.begin(), left.end());
        arr.push_back(fixed);
        arr.insert(arr.end(), right.begin(), right.end());
        return arr; 
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

    mas = quickSort(mas);

    for (int i = 0; i < n; i++)
        out << mas[i] << " ";

    return 0;
}
