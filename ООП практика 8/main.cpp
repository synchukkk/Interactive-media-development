#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <iomanip>
#include <set>
using namespace std;

struct ParticipantKey {
    string number, surname, name;
    bool operator<(const ParticipantKey& other) const {
        return tie(number, surname, name) < tie(other.number, other.surname, other.name);
    }
};

int main() {
    ifstream fin("results.txt");
    if (!fin) {
        cerr << "Не вдалося відкрити файл results.txt" << endl;
        return 1;
    }
    string line;
    getline(fin, line); // заголовок
    vector<string> criteria;
    stringstream ss(line);
    string crit;
    while (getline(ss, crit, ';')) criteria.push_back(crit);

    // {учасник: {суддя: сума балів}}
    map<ParticipantKey, map<string, int>> participants;
    while (getline(fin, line)) {
        if (line.empty() || line.find("Учасників:") == 0) break;
        stringstream ls(line);
        string number, surname, name, criterion, judge, score_str;
        getline(ls, number, ';');
        getline(ls, surname, ';');
        getline(ls, name, ';');
        getline(ls, criterion, ';');
        getline(ls, judge, ';');
        getline(ls, score_str, ';');
        int score = stoi(score_str);
        ParticipantKey key{number, surname, name};
        participants[key][judge] += score;
    }
    // Розрахунок остаточних оцінок
    vector<pair<ParticipantKey, double>> results;
    for (const auto& p : participants) {
        vector<int> sums;
        for (const auto& j : p.second) sums.push_back(j.second);
        if (sums.size() < 3) continue;
        sort(sums.begin(), sums.end());
        double avg = 0;
        for (size_t i = 1; i + 1 < sums.size(); ++i) avg += sums[i];
        avg /= (sums.size() - 2);
        results.push_back({p.first, avg});
    }
    sort(results.begin(), results.end(), [](const auto& a, const auto& b) {
        return a.second > b.second;
    });
    cout << left << setw(8) << "Номер" << setw(16) << "Прізвище" << setw(12) << "Ім'я" << "Остаточна оцінка" << endl;
    for (const auto& r : results) {
        cout << left << setw(8) << r.first.number << setw(16) << r.first.surname << setw(12) << r.first.name << fixed << setprecision(2) << r.second << endl;
    }
    return 0;
}
