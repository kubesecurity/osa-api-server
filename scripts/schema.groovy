        mgmt = graph.openManagement();

        // SecurityEvent
        event_type = mgmt.getPropertyKey('event_type');
        if(event_type == null) {
            event_type = mgmt.makePropertyKey('event_type').dataType(String.class).make();
        }

        body = mgmt.getPropertyKey('body');
        if(body == null) {
            body = mgmt.makePropertyKey('body').dataType(String.class).make();
        }

        title = mgmt.getPropertyKey('title');
        if(title == null) {
            title = mgmt.makePropertyKey('title').dataType(String.class).make();
        }

        url = mgmt.getPropertyKey('url');
        if(url == null) {
            url = mgmt.makePropertyKey('url').dataType(String.class).make();
        }

        status = mgmt.getPropertyKey('status');
        if(status == null) {
            status = mgmt.makePropertyKey('status').dataType(String.class).make();
        }

        event_id = mgmt.getPropertyKey('event_id');
        if(event_id == null) {
            event_id = mgmt.makePropertyKey('event_id').dataType(String.class).make();
        }

        created_at = mgmt.getPropertyKey('created_at');
        if(created_at == null) {
            created_at = mgmt.makePropertyKey('created_at').dataType(Integer.class).make();
        }

        updated_at = mgmt.getPropertyKey('updated_at');
        if(updated_at == null) {
            updated_at = mgmt.makePropertyKey('updated_at').dataType(Integer.class).make();
        }

        closed_at = mgmt.getPropertyKey('closed_at');
        if(closed_at == null) {
            closed_at = mgmt.makePropertyKey('closed_at').dataType(Integer.class).make();
        }

        // Ecosystem
        ecosystem_name = mgmt.getPropertyKey('ecosystem_name');
        if(ecosystem_name == null) {
            ecosystem_name = mgmt.makePropertyKey('ecosystem_name').dataType(String.class).make();
        }

        // Feedback
        author = mgmt.getPropertyKey('author');
        if(author == null) {
            author = mgmt.makePropertyKey('author').dataType(String.class).make();
        }

        comments = mgmt.getPropertyKey('comments');
        if(comments == null) {
            comments = mgmt.makePropertyKey('comments').dataType(String.class).make();
        }

        feedback_type = mgmt.getPropertyKey('feedback_type');
        if(feedback_type == null) {
            feedback_type = mgmt.makePropertyKey('feedback_type').dataType(String.class).make();
        }

        feedback_url = mgmt.getPropertyKey('feedback_url');
        if(feedback_url == null) {
            feedback_url = mgmt.makePropertyKey('feedback_url').dataType(String.class).make();
        }

        // Dependency
        dependency_name = mgmt.getPropertyKey('dependency_name');
        if(dependency_name == null) {
            dependency_name = mgmt.makePropertyKey('dependency_name').dataType(String.class).make();
        }

        dependency_path = mgmt.getPropertyKey('dependency_path');
        if(dependency_path == null) {
            dependency_path = mgmt.makePropertyKey('dependency_path').dataType(String.class).make();
        }

        // Version
        version = mgmt.getPropertyKey('version');
        if(version == null) {
            version = mgmt.makePropertyKey('version').dataType(String.class).make();
        }

        // ProbableCVE
        probable_vuln_id = mgmt.getPropertyKey('probable_vuln_id');
        if(probable_vuln_id == null) {
            probable_vuln_id = mgmt.makePropertyKey('probable_vuln_id').dataType(String.class).make();
        }


        // Extra
        vertex_label = mgmt.getPropertyKey('vertex_label');
        if(vertex_label == null) {
            vertex_label = mgmt.makePropertyKey('vertex_label').dataType(String.class).make();
        }

        // ReportedCVE
        cve_id = mgmt.getPropertyKey('cve_id');
        if(cve_id == null) {
            cve_id = mgmt.makePropertyKey('cve_id').dataType(String.class).make();
        }

        cvss = mgmt.getPropertyKey('cvss');
        if(cvss == null) {
            cvss = mgmt.makePropertyKey('cvss').dataType(Float.class).make();
        }

        severity = mgmt.getPropertyKey('severity');
        if(severity == null) {
            severity = mgmt.makePropertyKey('severity').dataType(String.class).make();
        }

        // Uniqueness constrains
        if(mgmt.getGraphIndex('URLIndex') == null) {
            mgmt.buildIndex('URLIndex', Vertex.class).addKey(url).unique().buildCompositeIndex();
        }

        if(mgmt.getGraphIndex('FeedbackUniqueIndex') == null) {
            mgmt.buildIndex('FeedbackUniqueIndex', Vertex.class).addKey(author).addKey(feedback_url).unique().buildCompositeIndex();
        }

        // Indexes
        List<String> allKeys = [
                'vertex_label',
                'dependency_name',
                'dependency_path',
                'probable_vuln_id',
                'feedback_type'
                'status',
                'event_type'
        ]

        allKeys.each { k ->
            keyRef = mgmt.getPropertyKey(k);
            index_key = 'index_prop_key_'+k;
            if(mgmt.getGraphIndex(index_key) == null) {
                mgmt.buildIndex(index_key, Vertex.class).addKey(keyRef).buildCompositeIndex()
            }
        }

        mgmt.commit();
