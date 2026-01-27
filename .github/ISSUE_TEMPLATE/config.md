---
name: Config
about: Configuration, environment setup, and technical decisions
title: "[CONFIG] "
labels: ["config", "infrastructure", "2-week-mvp"]
assignees: []
---

## ⚙️ Configuration Type
- [ ] Environment variables
- [ ] Database connection
- [ ] Third-party service setup (Mobile money, Auth0, etc.)
- [ ] Secrets management
- [ ] Feature flags
- [ ] Build / deployment configuration
- [ ] Monitoring / logging setup
- [ ] CORS / security headers

## 📝 Details
Describe the configuration needed and where it applies (dev / staging / production).

## 🔒 Sensitive Data?
- [ ] Yes (requires secrets management)
- [ ] No (can be committed to git)

**If sensitive, how should this be stored?**
- Environment variables
- Secret vault (AWS Secrets Manager, Vault, etc.)
- .env file (dev only, not committed)

## 🔧 Implementation Steps
1. Step one
2. Step two
3. Verification step

## ✅ Verification Checklist
- [ ] Configuration applied successfully
- [ ] Services/APIs responding correctly
- [ ] No hardcoded secrets in code
- [ ] Works in all environments (dev / staging / prod)
- [ ] Rollback procedure documented

## 📚 Documentation
Link to or provide:
- Configuration file example
- Setup instructions
- Troubleshooting guide

## 🔗 Affected Services
Which backend/frontend services depend on this configuration?

## ⚠️ Impact
What breaks if this configuration is wrong?

## 👤 Owner
Who is responsible for maintaining this configuration?
