#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <queue>
#include <unordered_set>
#include <cstring>
#include <functional>

using namespace std;
using pos = pair<int64_t, int64_t>;

struct dfs_entry {
    pos p;
    int steps_left;
};

inline bool operator==(const dfs_entry& lhs, const dfs_entry& rhs) {
    return lhs.p.first == rhs.p.first && lhs.p.second == rhs.p.second;
}

struct dfs_entry_hash {
    size_t operator()(const dfs_entry &e) const noexcept {
        return e.p.first << 20 | e.p.second << 10;
    }
};

int64_t solve(const pos& start, const vector<string> inp) {
    unordered_set<dfs_entry, dfs_entry_hash> visited;
    queue<dfs_entry> q;
    q.push({start, 64});

    int64_t reachable = 0;

    // Perform dfs
    while (!q.empty()) {
        dfs_entry e = q.front();
        q.pop();

        if (e.steps_left < 0) {
            continue;
        }
        if (e.p.first < 0 || e.p.first >= static_cast<int64_t>(inp.size())
                || e.p.second < 0 || e.p.second >= static_cast<int64_t>(inp[0].size())) {
            // Out of bounds
            continue;
        }
        if (inp[static_cast<size_t>(e.p.first)][static_cast<size_t>(e.p.second)] == '#') {
            continue;
        }

        if (visited.count(e) > 0) {
            continue;
        }
        visited.insert(e);

        reachable += static_cast<int64_t>(e.steps_left % 2 == 0);

        q.push({{e.p.first + 1, e.p.second}, e.steps_left - 1});
        q.push({{e.p.first - 1, e.p.second}, e.steps_left - 1});
        q.push({{e.p.first, e.p.second + 1}, e.steps_left - 1});
        q.push({{e.p.first, e.p.second - 1}, e.steps_left - 1});
    }

    return reachable;
}

int main(int argc, char** argv) {
    // Get input

    if (argc != 2) {
        cerr << "Specify input" << endl;
        exit(EXIT_FAILURE);
    }
    vector<string> inp;

    ifstream ifs(string(argv[1]), ifstream::in);
    string line;
    while (getline(ifs, line)) {
        inp.push_back(line);
    }

    // Solve 1

    // Find S
    pos start;
    for (size_t x = 0; x < inp.size(); x++) {
        for (size_t y = 0; y < inp[0].size(); y++) {
            if (inp[x][y] == 'S') {
                start = {x, y};
            }
        }
    }

    cout << solve(start, inp) << endl;
}
