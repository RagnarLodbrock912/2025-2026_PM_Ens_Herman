#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <algorithm> 
#include <numeric>

#define START_RUN_SIZE 2

using namespace std;

struct FileRun {
    std::string name;
    int runs;
    int size;
};

int nearestFib(int n) {
    vector<int> fib = {1, 1};
    while (fib.back() < n) {
        fib.push_back(fib.back() + fib[fib.size() - 2]);
    }
    return fib[fib.size() - 2];
}

int sumRuns(int sum, const FileRun& f) {
    return sum + f.runs;
}

bool compareRuns(const FileRun& a, const FileRun& b) {
    return a.runs < b.runs;
}

void mergeRuns(ifstream& in1, ifstream& in2, ofstream& out, int runSize1, int runSize2) {
    int count1 = 0, count2 = 0;
    int val1, val2;
    bool has1 = false, has2 = false;

    if (count1 < runSize1 && (in1 >> val1)) { has1 = true; count1++; }
    if (count2 < runSize2 && (in2 >> val2)) { has2 = true; count2++; }

    while (has1 || has2) {
        if (has1 && (!has2 || val1 <= val2)) {
            out << val1 << " ";
            if (count1 < runSize1 && (in1 >> val1)) { count1++; }
            else { has1 = false; }
        } else {
            out << val2 << " ";
            if (count2 < runSize2 && (in2 >> val2)) { count2++; }
            else { has2 = false; }
        }
    }
}

void externalMergeSort(string filename) {
    ifstream startFile(filename);
    ofstream f1("../f1.txt");
    ofstream f2("../f2.txt");

    if (!startFile.is_open()) {
        cerr << "Error opening file!" << endl;
        return;
    }

    int n, k;

    startFile >> n >> k;

    int el, amRuns1 = nearestFib(k);
    vector<int> arr;

    for (int i = 0; i < amRuns1; i++) {
        arr.clear();
        for (int j = 0; j < START_RUN_SIZE; j++) {
            startFile >> el;
            arr.push_back(el);
        }
        
        sort(arr.begin(), arr.end());

        for (int j = 0; j < START_RUN_SIZE; j++) {
            f1 << arr[j] << " ";
        }

    }

    for (int i = 0; i < k - amRuns1; i++) {
        arr.clear();
        for (int j = 0; j < START_RUN_SIZE; j++) {
            startFile >> el;
            arr.push_back(el);
        }

        sort(arr.begin(), arr.end());

        for (int j = 0; j < START_RUN_SIZE; j++) {
            f2 << arr[j] << " ";
        }

    }

    startFile.close();
    f1.close();
    f2.close();

    vector<FileRun> files = {
        {"../f1.txt", amRuns1, START_RUN_SIZE},
        {"../f2.txt", k - amRuns1, START_RUN_SIZE},
        {"../f3.txt", 0, 0}
    };

    while (std::accumulate(files.begin(), files.end(), 0, sumRuns) != 1) {
        std::sort(files.begin(), files.end(), compareRuns);

        ofstream out(files[0].name);
        ifstream in1(files[1].name);
        ifstream in2(files[2].name);

        for (int r = 0; r < files[1].runs; r++) {
            mergeRuns(in1, in2, out, files[1].size, files[2].size);
        }

        out.close();
        in1.close();

        ofstream out1(files[1].name);
        int val;

        while (in2 >> val) {
            out1 << val << " ";
        }

        in2.close();
        ofstream out2(files[2].name);
        out1.close();
        out2.close();


        files[0].runs = files[1].runs;
        files[0].size = files[1].size * 2;
        files[1].runs = files[2].runs - files[1].runs;
        files[1].size = files[2].size;
        files[2].runs = 0;
        files[2].size = 0;
    }
}

int main () {
    externalMergeSort("../input.txt");
    return 0;
}
