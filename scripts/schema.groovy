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

        closed_at = mgmt.getPropertyKey('closed_at');
        if(closed_at == null) {
            closed_at = mgmt.makePropertyKey('closed_at').dataType(Integer.class).make();
        }

        probable_cve = mgmt.getPropertyKey('probable_cve');
        if(probable_cve == null) {
            probable_cve = mgmt.makePropertyKey('probable_cve').dataType(Boolean.class).make();
        }

        repo_name = mgmt.getPropertyKey('repo_name');
        if(repo_name == null) {
            repo_name = mgmt.makePropertyKey('repo_name').dataType(String.class).make();
        }

        repo_path = mgmt.getPropertyKey('repo_path');
        if(repo_path == null) {
            repo_path = mgmt.makePropertyKey('repo_path').dataType(String.class).make();
        }

        ecosystem = mgmt.getPropertyKey('ecosystem');
        if(ecosystem == null) {
            ecosystem = mgmt.makePropertyKey('ecosystem').dataType(String.class).cardinality(Cardinality.SET).make();
        }

        creator_name = mgmt.getPropertyKey('creator_name');
        if(creator_name == null) {
            creator_name = mgmt.makePropertyKey('creator_name').dataType(String.class).make();
        }

        overall_feedback = mgmt.getPropertyKey('overall_feedback');
        if(overall_feedback == null) {
            overall_feedback = mgmt.makePropertyKey('overall_feedback').dataType(String.class).make();
        }

        feedback_count = mgmt.getPropertyKey('feedback_count');
        if(feedback_count == null) {
            feedback_count = mgmt.makePropertyKey('feedback_count').dataType(Integer.class).make();
        }

        updated_at = mgmt.getPropertyKey('updated_at');
        if(updated_at == null) {
            updated_at = mgmt.makePropertyKey('updated_at').dataType(Integer.class).make();
        }

        updated_date = mgmt.getPropertyKey('updated_date');
        if(updated_date == null) {
            updated_date = mgmt.makePropertyKey('updated_date').dataType(Integer.class).make();
        }

        updated_yearmonth = mgmt.getPropertyKey('updated_yearmonth');
        if(updated_yearmonth == null) {
            updated_yearmonth = mgmt.makePropertyKey('updated_yearmonth').dataType(Integer.class).make();
        }

        updated_month = mgmt.getPropertyKey('updated_month');
        if(updated_month == null) {
            updated_month = mgmt.makePropertyKey('updated_month').dataType(Integer.class).make();
        }

        updated_year = mgmt.getPropertyKey('updated_year');
        if(updated_year == null) {
            updated_year = mgmt.makePropertyKey('updated_year').dataType(Integer.class).make();
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

        // Extra
        vertex_label = mgmt.getPropertyKey('vertex_label');
        if(vertex_label == null) {
            vertex_label = mgmt.makePropertyKey('vertex_label').dataType(String.class).make();
        }

        // Uniqueness constrains
        if(mgmt.getGraphIndex('EcosystemURLUniqueIndex') == null) {
            mgmt.buildIndex('EcosystemURLUniqueIndex', Vertex.class).addKey(url).unique().buildCompositeIndex();
        }

        if(mgmt.getGraphIndex('FeedbackUniqueIndex') == null) {
            mgmt.buildIndex('FeedbackUniqueIndex', Vertex.class).addKey(author).addKey(feedback_url).unique().buildCompositeIndex();
        }

        if(mgmt.getGraphIndex('EcoPCVECompositeIndex') == null) {
            mgmt.buildIndex('EcoPCVECompositeIndex', Vertex.class).addKey(ecosystem).addKey(probable_cve).buildCompositeIndex();
        }

        if(mgmt.getGraphIndex('EcoPCVEUpdatedYearMonthCompositeIndex') == null) {
            mgmt.buildIndex('EcoPCVEUpdatedYearMonthCompositeIndex', Vertex.class).addKey(ecosystem).addKey(probable_cve).addKey(updated_yearmonth).buildCompositeIndex();
        }

        if(mgmt.getGraphIndex('EcoPCVEUpdatedDateCompositeIndex') == null) {
            mgmt.buildIndex('EcoPCVEUpdatedDateCompositeIndex', Vertex.class).addKey(ecosystem).addKey(probable_cve).addKey(updated_date).buildCompositeIndex();
        }

        if(mgmt.getGraphIndex('EcoPCVERepoNameCompositeIndex') == null) {
            mgmt.buildIndex('EcoPCVERepoNameCompositeIndex', Vertex.class).addKey(ecosystem).addKey(probable_cve).addKey(repo_name).buildCompositeIndex();
        }

        // Indexes
        List<String> allKeys = [
                'vertex_label',
                'event_type',
                'feedback_count',
                'overall_feedback',
                'updated_year',
                'updated_yearmonth',
                'updated_date',
                'probable_cve',
                'status',
                'repo_name',
                'creator_name',
                'author'
        ]

        allKeys.each { k ->
            keyRef = mgmt.getPropertyKey(k);
            index_key = 'index_prop_key_'+k;
            if(mgmt.getGraphIndex(index_key) == null) {
                mgmt.buildIndex(index_key, Vertex.class).addKey(keyRef).buildCompositeIndex()
            }
        }

        mgmt.commit();
