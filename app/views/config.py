configuration = {
	"view-access": {
		"public": {
			'login_required': 'false',
			'profile': []
		},
		"authorized": {
			'login_required': 'true',
			'profile': ['Profile']
		},
		"private": {
			'login_required': 'true',
			'profile': ['Admin']
		}
	},
	"views": {
		"activities": {
			"url-prefix": "activities",
			"page-types": ["Activity"]
		},
		"destinations": {
			"url-prefix": "destinations",
			"page-types": ["Destination"]
		},
		"articles": {
			"url-prefix": "articles",
			"page-types": ["Blog", "FitrangiSpecial"]
		},
		"events": {
			"url-prefix": "events",
			"page-types": ["Event"]
		},
		"orgainsers": {
			"url-prefix": "organisers",
			"page-types": ["EventOrganiser"]
		},
		"dealers": {
			"url-prefix": "dealers",
			"page-types": ["Retailer"]
		},
	},
	"templates": {
		"user": {
			"page-types": ["EventOrganiser", "Retailer"]
		},
		"post": {
			"page-types": ["Activity", "Destination", "Blog", "FitrangiSpecial"]
		}
	},
        "editors": {
                "login": {
                        "url-prefix": "/login",
                        "page-type":  "Profile",
                        "fields": {
                                "email":    {"required": True},
                                "password": {"required": True}
                        }
                },
                "logout": {
                        "url-prefix": "/login",
                        "page-type":  "Profile",
                        "fields": {}
                },
                "registration": {
                        "url-prefix": "/register",
                        "page-type":  "Profile",
                        "fields": {
                                "name":     {"required": True},
                                "email":    {"required": True},
                                "password": {"required": True},
                                "confirm":  {"required": True}
                        }
                }
        }
}
