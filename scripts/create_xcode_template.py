#!/usr/bin/env python3
"""
Create a minimal but valid Xcode project template for SwiftUI iOS apps.
Generates ThielonApp.xcodeproj with a project.pbxproj that can be copied and customized.
"""

import os
import uuid
import sys
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent.parent / 'templates' / 'ios'
APP_DIR = TEMPLATE_DIR / 'ThielonApp'
XCODEPROJ_DIR = TEMPLATE_DIR / 'ThielonApp.xcodeproj'

def generate_uuid(prefix=''):
    """Generate a deterministic-ish UUID based on prefix"""
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # NS_NAMESPACE_DNS
    return str(uuid.uuid5(namespace, prefix)).upper().replace('-', '')[:24]

def get_files():
    """Collect all Swift and resource files from the template app directory"""
    swift_files = []
    resource_files = []
    for root, dirs, files in os.walk(APP_DIR):
        for f in files:
            rel_path = Path(root).relative_to(APP_DIR) / f
            rel_str = str(rel_path).replace('\\', '/')
            if f.endswith('.swift'):
                swift_files.append(rel_str)
            else:
                resource_files.append(rel_str)
    # Sort for consistency
    swift_files.sort()
    resource_files.sort()
    all_files = swift_files + resource_files
    return all_files, swift_files, resource_files

def create_pbxproj():
    """Generate the project.pbxproj content as a string"""
    all_files, swift_files, resource_files = get_files()
    
    # Generate UUIDs
    root_object_uuid = generate_uuid('RootObject')
    project_uuid = generate_uuid('PBXProject')
    main_group_uuid = generate_uuid('MainGroup')
    app_group_uuid = generate_uuid('AppGroup')
    config_list_uuid = generate_uuid('ProjectConfigList')
    target_config_list_uuid = generate_uuid('TargetConfigList')
    debug_conf_uuid = generate_uuid('DebugConfiguration')
    release_conf_uuid = generate_uuid('ReleaseConfiguration')
    target_debug_uuid = generate_uuid('TargetDebugConfiguration')
    target_release_uuid = generate_uuid('TargetReleaseConfiguration')
    sources_phase_uuid = generate_uuid('SourcesBuildPhase')
    resources_phase_uuid = generate_uuid('ResourcesBuildPhase')
    frameworks_phase_uuid = generate_uuid('FrameworksBuildPhase')
    target_uuid = generate_uuid('PBXNativeTarget')
    product_file_ref_uuid = generate_uuid('ProductFileReference')
    
    # Build file references
    file_ref_uuids = {}   # file_path -> uuid
    build_file_uuids = {} # file_path -> uuid (for swift only)
    build_file_list = []  # list of (build_file_uuid, file_ref_uuid) for swift
    
    for file_path in all_files:
        f_uuid = generate_uuid(f'FileRef-{file_path}')
        file_ref_uuids[file_path] = f_uuid
        if file_path.endswith('.swift'):
            b_uuid = generate_uuid(f'BuildFile-{file_path}')
            build_file_uuids[file_path] = b_uuid
            build_file_list.append((b_uuid, f_uuid))
    
    # Construct objects dictionary
    objects = {}
    
    # Root workspace
    objects[root_object_uuid] = {
        'isa': 'PBXWorkspace',
        'mainGroup': main_group_uuid,
        'children': [project_uuid]
    }
    
    # Project
    objects[project_uuid] = {
        'isa': 'PBXProject',
        'attributes': {
            'BuildIndependentTargetsInParallel': 1,
            'LastUpgradeCheck': 1200
        },
        'buildConfigurationList': config_list_uuid,
        'compatibilityVersion': 'Xcode 14.0',
        'developmentRegion': 'en',
        'hasScannedForEncodings': 0,
        'knownRegions': ['en', 'Base'],
        'mainGroup': main_group_uuid,
        'productRefGroup': main_group_uuid,
        'projectDirPath': '',
        'projectRoot': '',
        'targets': [target_uuid]
    }
    
    # Main group (root)
    objects[main_group_uuid] = {
        'isa': 'PBXGroup',
        'children': [app_group_uuid],
        'sourceTree': '<group>'
    }
    
    # App group (represents the app folder, e.g., ThielonApp/ or ResumeBuilder/)
    objects[app_group_uuid] = {
        'isa': 'PBXGroup',
        'name': 'ThielonApp',
        'path': 'ThielonApp',
        'children': [],  # populated below
        'sourceTree': '<group>'
    }
    
    # Add all file references to app group
    for file_path in all_files:
        objects[app_group_uuid]['children'].append(file_ref_uuids[file_path])
    
    # File references
    for file_path in all_files:
        f_uuid = file_ref_uuids[file_path]
        name = Path(file_path).name
        if file_path.endswith('.swift'):
            ftype = 'sourcecode.swift'
        elif file_path == 'Info.plist':
            ftype = 'text.plist.xml'
        elif file_path == 'Assets.xcassets':
            ftype = 'folder.assetcatalog'
        else:
            ftype = 'text'
        objects[f_uuid] = {
            'isa': 'PBXFileReference',
            'lastKnownFileType': ftype,
            'name': name,
            'path': file_path,
            'sourceTree': '<group>'
        }
    
    # Build files (for Swift sources)
    for b_uuid, f_uuid in build_file_list:
        objects[b_uuid] = {
            'isa': 'PBXBuildFile',
            'fileRef': f_uuid
        }
    
    # Build phases
    objects[sources_phase_uuid] = {
        'isa': 'PBXSourcesBuildPhase',
        'buildActionMask': 2147483647,
        'files': [b_uuid for b_uuid, _ in build_file_list],
        'runOnlyForDeploymentPostprocessing': 0
    }
    objects[resources_phase_uuid] = {
        'isa': 'PBXResourcesBuildPhase',
        'buildActionMask': 2147483647,
        'files': [file_ref_uuids[f] for f in resource_files],
        'runOnlyForDeploymentPostprocessing': 0
    }
    objects[frameworks_phase_uuid] = {
        'isa': 'PBXFrameworksBuildPhase',
        'buildActionMask': 2147483647,
        'files': [],
        'runOnlyForDeploymentPostprocessing': 0
    }
    
    # Native target
    objects[target_uuid] = {
        'isa': 'PBXNativeTarget',
        'buildConfigurationList': target_config_list_uuid,
        'buildPhases': [sources_phase_uuid, resources_phase_uuid, frameworks_phase_uuid],
        'buildRules': [],
        'dependencies': [],
        'name': '$(PRODUCT_NAME)',
        'productName': '$(PRODUCT_NAME)',
        'productReference': product_file_ref_uuid,
        'productType': 'com.apple.product-type.application'
    }
    
    # Product file reference (the built .app)
    objects[product_file_ref_uuid] = {
        'isa': 'PBXFileReference',
        'explicitFileType': 'wrapper.application',
        'lastKnownFileType': 'wrapper.application',
        'name': '$(PRODUCT_NAME).app',
        'path': '$(PRODUCT_NAME).app',
        'sourceTree': 'BUILT_PRODUCTS_DIR'
    }
    
    # Configuration lists
    objects[config_list_uuid] = {
        'isa': 'XCConfigurationList',
        'buildConfigurations': [debug_conf_uuid, release_conf_uuid],
        'defaultConfigurationIsVisible': 0,
        'defaultConfigurationName': 'Release'
    }
    objects[target_config_list_uuid] = {
        'isa': 'XCConfigurationList',
        'buildConfigurations': [target_debug_uuid, target_release_uuid],
        'defaultConfigurationIsVisible': 0,
        'defaultConfigurationName': 'Release'
    }
    
    # Build configurations
    proj_settings_common = {
        'ALWAYS_EMBED_SWIFT_STANDARD_LIBRARIES': 'YES',
        'ASSETCATALOG_COMPILER_APPICON_NAME': 'AppIcon',
        'CLANG_ENABLE_MODULES': 'YES',
        'CURRENT_PROJECT_VERSION': '1',
        'DEVELOPMENT_ASSET_PATHS': '',
        'ENABLE_PREVIEWS': 'YES',
        'GENERATE_INFOPLIST_FILE': 'NO',
        'INFOPLIST_FILE': 'ThielonApp/Info.plist',
        'INFOPLIST_KEY_CFBundleDisplayName': '$(PRODUCT_NAME)',
        'INFOPLIST_KEY_UISupportedInterfaceOrientations': 'UIInterfaceOrientationPortrait',
        'INFOPLIST_KEY_UISupportedInterfaceOrientations~ipad': '$(inherited) UIInterfaceOrientationPortrait UIInterfaceOrientationPortraitUpsideDown UIInterfaceOrientationLandscapeLeft UIInterfaceOrientationLandscapeRight',
        'LD_RUNPATH_SEARCH_PATHS': ['$(inherited)', '@executable_path/Frameworks', '@loader_path/Frameworks'],
        'MARKETING_VERSION': '1.0.0',
        'PRODUCT_BUNDLE_IDENTIFIER': 'com.thielon.template',
        'PRODUCT_NAME': 'ThielonApp',
        'SWIFT_VERSION': '5.0',
        'TARGETED_DEVICE_FAMILY': '1,2',
        'VERSIONING_SYSTEM': 'apple-generic'
    }
    
    objects[debug_conf_uuid] = {
        'isa': 'XCBuildConfiguration',
        'buildSettings': dict(proj_settings_common, **{
            'SWIFT_ACTIVE_COMPILATION_CONDITIONS': '$(inherited) DEBUG',
            'SWIFT_OPTIMIZATION_LEVEL': '-Onone'
        }),
        'name': 'Debug'
    }
    objects[release_conf_uuid] = {
        'isa': 'XCBuildConfiguration',
        'buildSettings': dict(proj_settings_common, **{
            'SWIFT_OPTIMIZATION_LEVEL': '-O'
        }),
        'name': 'Release'
    }
    
    target_settings_common = {
        'ASSETCATALOG_COMPILER_APPICON_NAME': 'AppIcon',
        'CODE_SIGN_STYLE': 'Automatic',
        'CURRENT_PROJECT_VERSION': '1',
        'DEVELOPMENT_ASSET_PATHS': '',
        'ENABLE_PREVIEWS': 'YES',
        'GENERATE_INFOPLIST_FILE': 'NO',
        'INFOPLIST_FILE': 'ThielonApp/Info.plist',
        'LD_RUNPATH_SEARCH_PATHS': ['$(inherited)', '@executable_path/Frameworks', '@loader_path/Frameworks'],
        'MARKETING_VERSION': '1.0.0',
        'PRODUCT_BUNDLE_IDENTIFIER': 'com.thielon.template',
        'PRODUCT_NAME': 'ThielonApp',
        'SWIFT_VERSION': '5.0',
        'TARGETED_DEVICE_FAMILY': '1,2'
    }
    
    objects[target_debug_uuid] = {
        'isa': 'XCBuildConfiguration',
        'buildSettings': dict(target_settings_common, **{
            'CODE_SIGN_IDENTITY': 'Apple Development',
            'SWIFT_ACTIVE_COMPILATION_CONDITIONS': '$(inherited) DEBUG',
            'SWIFT_OPTIMIZATION_LEVEL': '-Onone'
        }),
        'name': 'Debug'
    }
    objects[target_release_uuid] = {
        'isa': 'XCBuildConfiguration',
        'buildSettings': dict(target_settings_common, **{
            'CODE_SIGN_IDENTITY': 'Apple Distribution',
            'SWIFT_OPTIMIZATION_LEVEL': '-O'
        }),
        'name': 'Release'
    }
    
    # Serialize to pbxproj format
    lines = ['// !$*UTF8*$!', '{', '    archiveVersion = 1;', '    classes = {', '    };', '    objectVersion = 55;', '    objects = {']
    
    def value_str(v):
        if isinstance(v, str):
            return v
        elif isinstance(v, list):
            return '( ' + ', '.join(value_str(x) for x in v) + ' )'
        elif isinstance(v, dict):
            # Unlikely inline
            return '{ }'
        else:
            return str(v)
    
    for obj_id in sorted(objects.keys()):
        obj = objects[obj_id]
        # Choose a comment
        comment = obj.get('name', obj.get('path', obj.get('isa', 'object')))
        lines.append(f'        {obj_id} /* {comment} */ = {{')
        for key, val in obj.items():
            if key == 'id':
                continue
            if isinstance(val, str):
                lines.append(f'            {key} = {val};')
            elif isinstance(val, list):
                lines.append(f'            {key} = {value_str(val)};')
            elif isinstance(val, dict):
                dict_lines = []
                for k2, v2 in val.items():
                    if isinstance(v2, list):
                        dict_lines.append(f'                {k2} = {value_str(v2)};')
                    else:
                        dict_lines.append(f'                {k2} = {v2};')
                lines.append('            {')
                lines.extend(dict_lines)
                lines.append('            };')
        lines.append('        };')
    
    lines.append('    };')
    lines.append(f'    rootObject = {root_object_uuid};')
    lines.append('}')
    return '\n'.join(lines)

def main():
    if not APP_DIR.exists():
        print(f"Error: Template iOS app directory not found: {APP_DIR}")
        sys.exit(1)
    
    # Create .xcodeproj directory
    if XCODEPROJ_DIR.exists():
        print(f"Warning: {XCODEPROJ_DIR} already exists, overwriting")
        shutil.rmtree(XCODEPROJ_DIR)  # Need shutil
    XCODEPROJ_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create project.pbxproj
    pbxproj_path = XCODEPROJ_DIR / 'project.pbxproj'
    pbx_content = create_pbxproj()
    pbxproj_path.write_text(pbx_content)
    print(f"Created {pbxproj_path}")
    
    # Create workspace
    workspace_dir = XCODEPROJ_DIR / 'project.xcworkspace'
    if workspace_dir.exists():
        shutil.rmtree(workspace_dir)
    workspace_dir.mkdir(parents=True)
    workspace_file = workspace_dir / 'contents.xcworkspacedata'
    workspace_file.write_text('''<?xml version="1.0" encoding="UTF-8"?>
<Workspace
   version = "1.0">
   <FileRef
      location = "group:ThielonApp.xcodeproj">
   </FileRef>
</Workspace>''')
    print(f"Created {workspace_file}")
    
    # Create shared data
    shared_dir = XCODEPROJ_DIR / 'xcshareddata'
    shared_dir.mkdir(exist_ok=True)
    workspace_settings = shared_dir / 'WorkspaceSettings.xcsettings'
    workspace_settings.write_text('''<?xml version="1.0" encoding="UTF-8"?>
<WorkspaceSettings
   version = "1.0">
</WorkspaceSettings>''')
    print(f"Created {workspace_settings}")
    
    print("\n✅ Xcode project template created successfully!")

if __name__ == '__main__':
    import shutil
    main()
