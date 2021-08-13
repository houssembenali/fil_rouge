def test_create_bucket(test_client):

    response = test_client.get('/parametrage-cloud')
    assert response.status_code == 200
    #assert b'Paramétrage stockage cloud' in response.data
    assert b'Enregistrer' in response.data

def test_valid_create_bucket(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/parametrage-cloud' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/parametrage-cloud',
                                data=dict(namebucket='testbucket-1'),
                                follow_redirects=True)
    assert response.status_code == 200
    #assert b'Succès Création du Bucket testbucket-1' in response.data