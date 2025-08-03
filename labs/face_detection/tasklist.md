# 📋 Tasklist - Reorganize Face Detection Directory Structure

## 🎯 Overview
Hiện tại thư mục `labs/face_detection` có quá nhiều file lộn xộn. Cần sắp xếp lại thành các thư mục riêng biệt để dễ quản lý và bảo trì.

## 📊 Current Analysis
- **Total files**: ~150+ files
- **File types**: Scripts, documentation, images, logs, tests, configs
- **Issues**: Mixed file types, no clear organization, hard to navigate

## 🗂️ Proposed Directory Structure

### 1. `/scripts/` - All executable scripts
```
scripts/
├── startup/
│   ├── start_all.py
│   ├── start_backend.py
│   ├── start_frontend.py
│   ├── start_frontend_only.py
│   ├── start_frontend_background.py
│   ├── start_fe.py
│   ├── quick_start_fe.py
│   └── start_api_server.py
├── management/
│   ├── manage_frontend.py
│   ├── stop_frontend.py
│   ├── stop_all.py
│   └── list_scripts.py
├── debugging/
│   ├── debug_camera_permissions.py
│   ├── debug_camera_restart.py
│   ├── debug_camera_stream.py
│   ├── debug_auto_recognition.py
│   ├── debug_recognition_error.py
│   ├── debug_bounding_box.py
│   ├── debug_bounding_box_alignment.py
│   ├── debug_bounding_box_analysis.py
│   ├── debug_scaling_issue.py
│   ├── debug_logging.py
│   ├── debug_api.py
│   └── debug_recognition.py
├── testing/
│   ├── test_auto_recognition.py
│   ├── test_auto_recognition_real_face.py
│   ├── test_bounding_box.py
│   ├── test_bounding_box_accuracy.py
│   ├── test_bounding_box_original.py
│   ├── test_camera_control.py
│   ├── test_camera_control_fix.py
│   ├── test_cropped_face_recognition.py
│   ├── test_delete_and_image_workflow.py
│   ├── test_face_list_load.py
│   ├── test_frontend_alignment.py
│   ├── test_frontend_coordinates.py
│   ├── test_frontend_face_list.py
│   ├── test_modern_refresh_button.py
│   ├── test_real_face.py
│   ├── test_real_face_detection.py
│   ├── test_real_face_fixed.py
│   ├── test_real_workflow.py
│   ├── test_realtime_detection.py
│   ├── test_refresh_button.py
│   ├── test_registration_workflow.py
│   ├── test_scaling_fix.py
│   ├── test_simple.py
│   ├── test_table_layout.py
│   ├── test_webcam_recognition.py
│   ├── test_with_content_type.py
│   ├── test_with_real_image.py
│   ├── test_with_realistic_face.py
│   ├── test_workflow.py
│   └── test_workflow_steps.py
├── tools/
│   ├── check_cameras.py
│   ├── fix_camera_config.py
│   ├── load_test.py
│   ├── monitoring.py
│   ├── performance_test.py
│   ├── security_test.py
│   ├── service_check.py
│   ├── service_check_fixed.py
│   ├── simple_test.py
│   ├── stable_server.py
│   └── test_realtime_recognition.py
└── deployment/
    ├── deploy.sh
    ├── manage_resources.sh
    ├── auto_server.py
    ├── auto_test_runner.py
    └── complete_fix.py
```

### 2. `/docs/` - All documentation files
```
docs/
├── architecture/
│   ├── api-design.md
│   ├── database-schema.md
│   ├── dataflow-diagram.md
│   ├── system-architecture.md
│   ├── technical-specifications.md
│   └── workflow-diagram.md
├── summaries/
│   ├── auto_detection_workflow_analysis.md
│   ├── auto_recognition_debug_summary.md
│   ├── auto_recognition_summary.md
│   ├── bounding_box_alignment_fix.md
│   ├── bounding_box_fix_summary.md
│   ├── bounding_box_implementation.md
│   ├── bounding_box_original_fix.md
│   ├── bounding_box_solution.md
│   ├── camera_control_enhancement_summary.md
│   ├── camera_control_fix_summary.md
│   ├── camera_restart_fix_summary.md
│   ├── CHANGES_SUMMARY.md
│   ├── data_cleanup_summary.md
│   ├── debug_summary.md
│   ├── face_delete_and_image_summary.md
│   ├── face_list_debug_summary.md
│   ├── final_service_status.md
│   ├── final_success_report.md
│   ├── final_workflow_summary.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── modern_refresh_button_summary.md
│   ├── realtime_detection_summary.md
│   ├── recognition_debug_report.md
│   ├── refresh_button_summary.md
│   ├── registration_workflow_fix_summary.md
│   ├── scaling_fix_summary.md
│   ├── table_layout_summary.md
│   └── webcam_recognition_fix.md
├── guides/
│   ├── FINAL_DOCUMENTATION_UPDATE.md
│   ├── FINAL_SUMMARY.md
│   ├── FRONTEND_SCRIPTS.md
│   ├── FRONTEND_SUMMARY.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── PRODUCTION_DEPLOYMENT.md
│   ├── README.md
│   ├── README_STARTUP.md
│   ├── RESOURCES_README.md
│   └── shared_resources.md
└── plans/
    ├── auto_fix_plan.md
    ├── face_delete_and_image_tasklist.md
    ├── tasklist.md
    └── workflow_test_plan.md
```

### 3. `/assets/` - All images and media files
```
assets/
├── images/
│   ├── coordinate_test_image.jpg
│   ├── debug_face.jpg
│   ├── debug_real_face.jpg
│   ├── frontend_test_face.jpg
│   ├── ideal_face.jpg
│   ├── real_face.jpg
│   ├── realistic_face_test.jpg
│   ├── test_centered_face.jpg
│   ├── test_face.jpg
│   ├── test_known_face.jpg
│   ├── test_real_face.jpg
│   ├── test_recognition_realistic.jpg
│   └── test_realistic_face.jpg
└── data/
    ├── debug_results.json
    ├── debug_trace.log
    ├── real_test_results.json
    ├── realistic_test_results.json
    ├── service_check_20250731_221557.json
    ├── service_check_fixed_20250731_221704.json
    ├── startup_log_20250731_222327.txt
    ├── test_results.json
    └── auto_server.log
```

### 4. `/config/` - Configuration files
```
config/
├── config.py
├── requirements.txt
├── requirements_minimal.txt
├── setup.py
├── docker-compose.yml
├── Dockerfile
└── .github/
```

### 5. Keep existing directories
```
fe/                    # Frontend files (keep as is)
src/                   # Source code (keep as is)
tests/                 # Test files (keep as is)
uploads/               # Upload files (keep as is)
logs/                  # Log files (keep as is)
data/                  # Data files (keep as is)
automation_test/       # Automation tests (keep as is)
labs/                  # Lab files (keep as is)
```

## 📋 Implementation Tasks

### Phase 1: Create Directory Structure
- [ ] Create `/scripts/` directory and subdirectories
- [ ] Create `/docs/` directory and subdirectories  
- [ ] Create `/assets/` directory and subdirectories
- [ ] Create `/config/` directory
- [ ] Verify all directories are created correctly

### Phase 2: Move Files
- [ ] Move startup scripts to `/scripts/startup/`
- [ ] Move management scripts to `/scripts/management/`
- [ ] Move debugging scripts to `/scripts/debugging/`
- [ ] Move testing scripts to `/scripts/testing/`
- [ ] Move tool scripts to `/scripts/tools/`
- [ ] Move deployment scripts to `/scripts/deployment/`
- [ ] Move documentation files to `/docs/` subdirectories
- [ ] Move image files to `/assets/images/`
- [ ] Move data files to `/assets/data/`
- [ ] Move config files to `/config/`

### Phase 3: Update Internal Links
- [ ] Update all import statements in Python files
- [ ] Update all file path references
- [ ] Update documentation links
- [ ] Update script references
- [ ] Test all internal links work correctly

### Phase 4: Testing
- [ ] Test all startup scripts work from new locations
- [ ] Test all management scripts work from new locations
- [ ] Test all debugging scripts work from new locations
- [ ] Test all testing scripts work from new locations
- [ ] Test all tool scripts work from new locations
- [ ] Test all deployment scripts work from new locations
- [ ] Verify documentation links work correctly
- [ ] Test frontend and backend startup from new structure

### Phase 5: Documentation Update
- [ ] Update README.md with new structure
- [ ] Update all documentation files with new paths
- [ ] Create directory structure documentation
- [ ] Update script usage instructions
- [ ] Create migration guide

## ⚠️ Important Notes

### Before Moving Files:
1. **Backup current state**: Create backup of current directory
2. **Stop all running processes**: Ensure no scripts are running
3. **Check git status**: Ensure all changes are committed
4. **Test current functionality**: Verify everything works before moving

### During Moving:
1. **Update paths carefully**: Ensure all internal references are updated
2. **Test incrementally**: Test each category of files after moving
3. **Maintain permissions**: Ensure executable scripts remain executable
4. **Update shebang lines**: Update any hardcoded paths in scripts

### After Moving:
1. **Comprehensive testing**: Test all functionality
2. **Update documentation**: Update all references
3. **Commit changes**: Commit the new structure to git
4. **Update deployment**: Update any deployment scripts

## 🎯 Success Criteria
- [ ] All files organized in logical directories
- [ ] All internal links work correctly
- [ ] All scripts execute from new locations
- [ ] Documentation updated with new structure
- [ ] Git repository updated with new structure
- [ ] No broken functionality

## 📝 Migration Checklist
- [ ] Create backup
- [ ] Stop all running processes
- [ ] Create new directory structure
- [ ] Move files systematically
- [ ] Update all internal references
- [ ] Test all functionality
- [ ] Update documentation
- [ ] Commit changes to git
- [ ] Verify deployment still works
- [ ] Create final documentation update

---

**Status**: 🚧 Planning Phase
**Priority**: High
**Estimated Time**: 2-3 hours
**Dependencies**: None 