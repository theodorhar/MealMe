//
//  Repository.swift
//  MealME
//
//  Created by Tanay Kane on 2/1/20.
//  Copyright © 2020 Theodor Har. All rights reserved.
//

import Foundation
class Repository {
    var defaults: UserDefaults
    
    init() {
        // Creates a connection to UserDefaults
        defaults = UserDefaults.init(suiteName: "group.com")!
    }
    
    // Load
    //    Given a key, load the data assosiated with that key
    //    Returns value if it exist, else returns nil
    func load(key: String) -> Any? {
        return defaults.data(forKey: key)
    }
    
    // Save
    //    Saves a value to the given key in User.Defaults
    func save(key: String, value: Any) {
        defaults.set(value, forKey: key)
        defaults.synchronize()
    }
}
