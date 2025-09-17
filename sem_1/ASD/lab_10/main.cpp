#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>

using namespace std;

void mergeSort(vector<int>& arr) {
    int n = arr.size();
    vector<int> temp(n);

    for (int width = 1; width < n; width *= 2) {
        for (int i = 0; i < n; i += 2 * width) {
            int left = i;
            int mid = min(i + width, n);
            int right = min(i + 2 * width, n);

            int l = left, r = mid, t = left;

            while (l < mid && r < right)
                temp[t++] = (arr[l] < arr[r]) ? arr[l++] : arr[r++];

            while (l < mid)
                temp[t++] = arr[l++];

            while (r < right)
                temp[t++] = arr[r++];
        }

        arr = temp;
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

    mergeSort(mas);

    for (int i = 0; i < n; i++)
        out << mas[i] << " ";

    return 0;
}
