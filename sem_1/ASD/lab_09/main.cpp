#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

void siftDown(vector<int>& heap, int i, int heapSize)
{
    while (2 * i + 1 < heapSize)
    {
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        int j = left;
        if (right < heapSize && heap[right] > heap[left])
            j = right;
        if (heap[i] >= heap[j])
            break;
        swap(heap[i], heap[j]);
        i = j;
    }
}

void buildHeap(vector<int>& heap)
{
    for (int i = heap.size() / 2 - 1; i >= 0; i--)
        siftDown(heap, i, heap.size());
}

void heapSort(vector<int>& arr)
{
    buildHeap(arr);
    int heapSize = arr.size();
    for (int i = 0; i < arr.size(); i++)
    {
        swap(arr[0], arr[heapSize - 1]);
        heapSize--;
        siftDown(arr, 0, heapSize);
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

    heapSort(mas);

    for (int i = 0; i < n; i++)
        out << mas[i] << " ";

    return 0;
}
